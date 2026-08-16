#!/usr/bin/env python

import argparse
import base64
import logging
import os
import collections
import shutil
import subprocess
import sys
import threading
import time

import gitlab
import urllib3

from urllib.parse import urlparse, urlunparse

logger = logging.getLogger(__name__)

SECRET = "*****"

# How many trailing stderr lines to quote back when a git command fails
STDERR_TAIL_LINES = 5

# Reported when a git command is killed for exceeding --git-timeout
TIMEOUT_RETURNCODE = 124

# Nth retry waits N times this many seconds
RETRY_BACKOFF_SECONDS = 5

# A transfer below this many bytes/sec for --stall-timeout seconds is stalled
STALL_SPEED_BYTES = 1000

FILE_URI_PREFIX = "file://"


class GitCommandError(Exception):
    """Raised when a git subprocess exits non-zero."""


def remote_host(url):
    """The host a remote URL points at, or "" for a local path.

    Hosts are compared case-insensitively because DNS is.
    """
    if not url:
        return ""

    if "://" in url:
        return (urlparse(url).hostname or "").lower()

    # scp-like syntax: [user@]host:path
    head, sep, _tail = url.partition(":")
    if not sep or os.path.sep in head or "\\" in head:
        return ""
    # A lone letter before the colon is a Windows drive, not a host, which is
    # the same rule git itself applies
    if len(head) == 1 and head.isalpha():
        return ""
    return head.rpartition("@")[2].lower()


def remote_repo_path(url):
    """The project path a remote URL points at, ignoring transport and suffix.

    https://host/group/project.git and git@host:group/project both reduce to
    group/project, so switching --prefer-ssh is recognised as the same
    repository while a genuinely different project is not.
    """
    if not url:
        return ""

    path = urlparse(url).path if "://" in url else url.rpartition(":")[2]
    path = path.strip("/")
    if path.endswith(".git"):
        path = path[: -len(".git")]
    return path


def mask_command(popenargs):
    """Redact credentials from a command line before it is displayed.

    Tokens reach git through the environment, but a remote URL may still carry
    embedded credentials, and callers may pass -c http.extraHeader themselves.
    """
    masked = []
    for arg in popenargs:
        arg = str(arg)
        if "http.extraHeader=" in arg:
            prefix, _, _value = arg.partition("http.extraHeader=")
            masked.append("{0}http.extraHeader={1}".format(prefix, SECRET))
        elif "://" in arg:
            masked.append(mask_password(arg))
        else:
            masked.append(arg)
    return masked


def logging_subprocess(
    popenargs,
    stdout_log_level=logging.DEBUG,
    stderr_log_level=logging.ERROR,
    stderr_buffer=None,
    timeout=None,
    **kwargs
):
    """
    Variant of subprocess.call that accepts a logger instead of stdout/stderr,
    and logs stdout messages via logger.debug and stderr messages via
    logger.error.

    Pass a list as stderr_buffer to also collect the child's stderr lines, so
    a caller can quote them when the command fails. Pass timeout to bound how
    long the child may run; it is killed and TIMEOUT_RETURNCODE is returned.
    """
    child = subprocess.Popen(
        popenargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs
    )

    def log_output(pipe, log_level, buffer=None):
        # Drain the pipe from a thread so the child never blocks on a full
        # pipe buffer, logging each line as it arrives.
        with pipe:
            for line in iter(pipe.readline, b""):
                line = line.rstrip(b"\r\n")
                if buffer is not None:
                    buffer.append(line)
                try:
                    logger.log(log_level, line)
                except Exception:
                    # Keep draining even if logging fails, or the child
                    # blocks on a full pipe buffer again
                    pass

    threads = [
        threading.Thread(
            target=log_output, args=(child.stdout, stdout_log_level), daemon=True
        ),
        threading.Thread(
            target=log_output,
            args=(child.stderr, stderr_log_level, stderr_buffer),
            daemon=True,
        ),
    ]
    for thread in threads:
        thread.start()

    try:
        rc = child.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        logger.error(
            "{0} exceeded the {1}s timeout, terminating it".format(
                " ".join(mask_command(popenargs)), timeout
            )
        )
        child.kill()
        child.wait()
        rc = TIMEOUT_RETURNCODE

    # Timeout in case a grandchild inherited the pipe handles and keeps
    # them open past the child's exit, which would delay EOF indefinitely
    for thread in threads:
        thread.join(timeout=60)

    if rc != 0:
        print("{} returned {}:".format(popenargs[0], rc), file=sys.stderr)
        print("\t", " ".join(mask_command(popenargs)), file=sys.stderr)

    return rc


def run_git(popenargs, retries=0, retry_if=None, **kwargs):
    """Run a git command, raising GitCommandError if it fails.

    Every git failure has to surface: a backup that silently skipped half its
    repositories is worse than one that reports an error.

    git writes ordinary progress to stderr, so those lines are logged at debug
    level and only quoted back at error level if the command actually fails.

    A failed command is retried up to `retries` times with a widening pause, so
    one network blip does not fail an otherwise healthy repository. Pass
    retry_if to veto a retry that would not be safe to repeat.
    """
    kwargs.setdefault("stderr_log_level", logging.DEBUG)

    attempt = 0
    while True:
        # Bounded: a chatty git command can emit millions of stderr lines and
        # only the tail is ever quoted back
        stderr_lines = collections.deque(maxlen=STDERR_TAIL_LINES)
        rc = logging_subprocess(popenargs, stderr_buffer=stderr_lines, **kwargs)
        if rc == 0:
            return rc

        if attempt >= retries or (retry_if is not None and not retry_if()):
            detail = ""
            if stderr_lines:
                tail = [line.decode("utf-8", "replace") for line in stderr_lines]
                detail = ": {0}".format(" / ".join(tail))
            raise GitCommandError(
                "{0} exited with code {1}{2}".format(
                    " ".join(mask_command(popenargs)), rc, detail
                )
            )

        attempt += 1
        pause = RETRY_BACKOFF_SECONDS * attempt
        logger.warning(
            "{0} exited with code {1}, retrying in {2}s ({3} of {4})".format(
                " ".join(mask_command(popenargs)), rc, pause, attempt, retries
            )
        )
        time.sleep(pause)


def mkdir_p(*args):
    for path in args:
        os.makedirs(path, exist_ok=True)


def mask_password(url, secret=SECRET):
    """Redact the credential in a URL, leaving the rest of it readable.

    Only the userinfo section is rewritten. A blind substring replace would
    also hit the host and path whenever the password happens to appear there,
    destroying the very detail the log line exists to convey.
    """
    parsed = urlparse(url)

    if not parsed.password:
        return url

    userinfo, _, hostport = parsed.netloc.rpartition("@")
    username, _, _password = userinfo.partition(":")

    if parsed.password == "x-oauth-basic":
        # The token is the username in this scheme
        masked_userinfo = "{0}:{1}".format(secret, parsed.password)
    else:
        masked_userinfo = "{0}:{1}".format(username, secret)

    return urlunparse(
        parsed._replace(netloc="{0}@{1}".format(masked_userinfo, hostport))
    )


def read_token(value):
    """Resolve a token that may be given inline or as file://path."""
    if value and value.startswith(FILE_URI_PREFIX):
        with open(value[len(FILE_URI_PREFIX) :], "rt") as f:
            return f.readline().strip()
    return value


def should_include_repository(args, attributes):
    """Whether a project falls under the requested --namespace.

    A namespace covers its subgroups, so --namespace group also backs up
    group/subgroup/project.
    """
    if not args.namespace:
        return True

    full_path = attributes["namespace"]["full_path"]
    if full_path == args.namespace or full_path.startswith(args.namespace + "/"):
        return True

    logger.debug(
        "Skipping {0} as namespace does not match {1}".format(
            attributes["path_with_namespace"], args.namespace
        )
    )
    return False


def get_git_env(args):
    """Build the environment for git subprocesses.

    The credential travels in GIT_CONFIG_* rather than on the command line so
    it does not appear in `ps` output. Requires git 2.31+.
    """
    env = os.environ.copy()
    entries = []

    token = read_token(args.private_token or args.oauth_token)
    if token:
        auth_pair = "oauth2:{0}".format(token).encode("utf-8")
        b64_auth = base64.b64encode(auth_pair).decode("utf-8")
        entries.append(
            ("http.extraHeader", "Authorization: Basic {0}".format(b64_auth))
        )

    # Abandon an HTTP transfer that has stalled rather than one that is merely
    # slow, so a large repository still downloads but a dead connection does
    # not hang the run for ever
    stall_timeout = getattr(args, "stall_timeout", 0)
    if stall_timeout:
        entries.append(("http.lowSpeedLimit", str(STALL_SPEED_BYTES)))
        entries.append(("http.lowSpeedTime", str(stall_timeout)))

    if not entries:
        return env

    try:
        count = int(env.get("GIT_CONFIG_COUNT", "0"))
    except ValueError:
        count = 0

    for key, value in entries:
        env["GIT_CONFIG_KEY_{0}".format(count)] = key
        env["GIT_CONFIG_VALUE_{0}".format(count)] = value
        count += 1

    env["GIT_CONFIG_COUNT"] = str(count)
    return env


def probe_remote(remote_url, git_env=None, timeout=None, retries=0):
    """Return git ls-remote's exit code, killing it if it exceeds timeout.

    subprocess.call would raise TimeoutExpired and leave the child running, so
    the hung git process would outlive the backup.

    Retried like the fetch and clone that follow it, so a blip on the
    reachability probe does not fail an otherwise healthy repository.
    """
    attempt = 0
    while True:
        child = subprocess.Popen(
            ["git", "ls-remote", remote_url],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=git_env,
        )
        try:
            rc = child.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            logger.error(
                "git ls-remote {0} exceeded the {1}s timeout, terminating it".format(
                    mask_password(remote_url), timeout
                )
            )
            child.kill()
            child.wait()
            rc = TIMEOUT_RETURNCODE

        if rc == 0 or attempt >= retries:
            return rc

        attempt += 1
        pause = RETRY_BACKOFF_SECONDS * attempt
        logger.warning(
            "git ls-remote {0} exited with code {1}, retrying in {2}s "
            "({3} of {4})".format(
                mask_password(remote_url), rc, pause, attempt, retries
            )
        )
        time.sleep(pause)


def non_negative_int(value):
    """argparse type for a count or a number of seconds.

    A negative timeout expires immediately, which would kill every git command
    the moment it starts, so reject it rather than let it through silently.
    """
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        raise argparse.ArgumentTypeError("{0!r} is not an integer".format(value))
    if parsed < 0:
        raise argparse.ArgumentTypeError("{0} must not be negative".format(parsed))
    return parsed


def check_git_install():
    try:
        exit_code = subprocess.call(
            ["git", "version"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except OSError:
        exit_code = 1
    if exit_code != 0:
        raise Exception(
            "git was not found on PATH. gitlab-backup shells out to git 2.31+ "
            "to clone and update repositories; install it and try again."
        )


def check_git_lfs_install():
    try:
        exit_code = subprocess.call(
            ["git", "lfs", "version"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except OSError:
        exit_code = 1
    if exit_code != 0:
        raise Exception(
            "The argument --clone-lfs requires you to have Git LFS installed.\n"
            "You can get it from https://git-lfs.github.com."
        )


def looks_like_repository(local_dir):
    """Whether a directory git refused to read still looks like a clone.

    Distinguishes a half-written clone worth reporting as such from an
    unrelated directory that merely occupies the path.
    """
    if os.path.exists(os.path.join(local_dir, ".git")):
        return True

    # A bare clone keeps these at the top level
    return all(
        os.path.exists(os.path.join(local_dir, marker))
        for marker in ("HEAD", "objects")
    )


def check_existing_clone(local_dir, bare_clone, git_env=None):
    """Whether local_dir holds a usable clone of the expected kind.

    A run killed part way through a clone leaves a directory with a .git entry
    that git cannot read. Left undetected it takes the update path on every
    later run, failing forever on a repository that only needs re-cloning, so
    ask git whether the directory is really a repository instead of trusting
    the presence of .git.
    """
    if not os.path.exists(local_dir):
        return False

    try:
        git_dir = (
            subprocess.check_output(
                ["git", "rev-parse", "--absolute-git-dir"],
                cwd=local_dir,
                stderr=subprocess.DEVNULL,
                env=git_env,
            )
            .decode("utf-8")
            .strip()
        )
    except (subprocess.CalledProcessError, NotADirectoryError):
        if looks_like_repository(local_dir):
            raise GitCommandError(
                "{0} looks like a repository but git cannot read it. A previous "
                "run may have been interrupted; remove the directory to have it "
                "cloned again".format(local_dir)
            )
        raise GitCommandError(
            "{0} exists but is not a git repository".format(local_dir)
        )

    # git discovery walks up the directory tree, so an output directory nested
    # inside an unrelated repository would otherwise look like our clone and we
    # would rewrite that repository's origin and fetch over it. Only accept a
    # git directory that is exactly where this clone should have put one.
    # A clone of the wrong kind fails the same comparison and is treated as
    # absent, matching the previous behaviour of re-cloning when --clone-bare
    # is turned on afterwards.
    expected = local_dir if bare_clone else os.path.join(local_dir, ".git")
    return os.path.realpath(git_dir) == os.path.realpath(expected)


def discard_partial_clone(local_dir, existed_before):
    """Remove a directory left behind by a clone that was killed.

    Returns whether the path is now clear, which is also the condition for
    retrying the clone.
    """
    # lexists, not exists: a broken symlink still occupies the path but would
    # otherwise look absent and the retry would fail on it
    if existed_before:
        return not os.path.lexists(local_dir)

    if os.path.lexists(local_dir):
        logger.warning("Removing partial clone at {0}".format(local_dir))
        if os.path.isdir(local_dir) and not os.path.islink(local_dir):
            shutil.rmtree(local_dir, ignore_errors=True)
        else:
            try:
                os.unlink(local_dir)
            except OSError:
                pass

    return not os.path.lexists(local_dir)


def assert_same_repository(
    local_dir, remote_url, git_env=None, allow_host_change=False
):
    """Refuse to fetch one project into another project's directory.

    On a case-insensitive filesystem Group/Project and group/project resolve to
    the same path, so the second would rewrite the first's origin and pull a
    different repository's refs over it.

    The host is compared too, since two instances can both hold group/project.
    Switching between https and ssh on one host stays allowed; a genuine
    instance rename needs --allow-host-change.
    """
    try:
        current = (
            subprocess.check_output(
                ["git", "remote", "get-url", "origin"],
                cwd=local_dir,
                stderr=subprocess.DEVNULL,
                env=git_env,
            )
            .decode("utf-8")
            .strip()
        )
    except subprocess.CalledProcessError:
        return

    if remote_repo_path(current) != remote_repo_path(remote_url):
        raise GitCommandError(
            "{0} already holds {1}, refusing to overwrite it with {2}. Two "
            "projects whose paths differ only in capitalisation share one "
            "directory on this filesystem; back them up to separate "
            "--output-directory paths".format(
                local_dir, mask_password(current), mask_password(remote_url)
            )
        )

    if not allow_host_change and remote_host(current) != remote_host(remote_url):
        raise GitCommandError(
            "{0} already holds {1}, refusing to overwrite it with {2}. The same "
            "project path exists on both hosts; back the two instances up to "
            "separate --output-directory paths, or pass --allow-host-change if "
            "the instance was renamed".format(
                local_dir, mask_password(current), mask_password(remote_url)
            )
        )


def fetch_repository(
    args,
    name,
    remote_url,
    local_dir,
    skip_existing=False,
    bare_clone=False,
    lfs_clone=False,
):
    git_env = get_git_env(args)

    retries = getattr(args, "retries", 0)
    timeout = getattr(args, "git_timeout", 0) or None

    clone_exists = check_existing_clone(local_dir, bare_clone, git_env)

    if clone_exists and skip_existing:
        return

    masked_remote_url = mask_password(remote_url)

    # An empty-but-existing repository answers ls-remote with an exit code of 0
    # and no refs, so a non-zero code always means the remote could not be read
    initialized = probe_remote(
        remote_url, git_env=git_env, timeout=timeout, retries=retries
    )
    if initialized != 0:
        raise GitCommandError(
            "Could not read {0} ({1}): git ls-remote exited with code {2}. "
            "The repository may be missing, private, or the credentials may be "
            "invalid".format(name, masked_remote_url, initialized)
        )

    if clone_exists:
        logger.info("Updating {0} in {1}".format(name, local_dir))

        try:
            remotes = subprocess.check_output(
                ["git", "remote", "show"], cwd=local_dir, env=git_env
            )
        except subprocess.CalledProcessError as e:
            raise GitCommandError(
                "Could not list the remotes of {0}: git remote show exited "
                "with code {1}".format(local_dir, e.returncode)
            )
        remotes = [i.strip() for i in remotes.decode("utf-8").splitlines()]

        if "origin" not in remotes:
            git_command = ["git", "remote", "add", "origin", remote_url]
            run_git(git_command, cwd=local_dir, env=git_env, timeout=timeout)
        else:
            assert_same_repository(
                local_dir,
                remote_url,
                git_env,
                allow_host_change=getattr(args, "allow_host_change", False),
            )
            git_command = ["git", "remote", "set-url", "origin", remote_url]
            run_git(git_command, cwd=local_dir, env=git_env, timeout=timeout)

        run_git(
            ["git", "fetch", "--all", "--force", "--tags", "--prune"],
            cwd=local_dir,
            env=git_env,
            retries=retries,
            timeout=timeout,
        )
    else:
        logger.info(
            "Cloning {0} repository from {1} to {2}".format(
                name, masked_remote_url, local_dir
            )
        )
        if bare_clone:
            git_command = ["git", "clone", "--mirror", remote_url, local_dir]
        else:
            git_command = ["git", "clone", remote_url, local_dir]
        # A clone killed by --git-timeout cannot clean up after itself, so
        # remove what it left behind. Only ever a directory this run created.
        existed_before = os.path.lexists(local_dir)
        try:
            run_git(
                git_command,
                env=git_env,
                retries=retries,
                retry_if=lambda: discard_partial_clone(local_dir, existed_before),
                timeout=timeout,
            )
        except GitCommandError:
            discard_partial_clone(local_dir, existed_before)
            raise

    # LFS objects are fetched in addition to the refs above, never instead of
    # them, otherwise a --clone-lfs backup would stop receiving new commits
    if lfs_clone:
        run_git(
            ["git", "lfs", "fetch", "--all", "--prune"],
            cwd=local_dir,
            env=git_env,
            retries=retries,
            timeout=timeout,
        )


def backup_repository(args, item):
    if not should_include_repository(args, item.attributes):
        return

    repo_name = item.path_with_namespace
    repo_cwd = os.path.join(args.output_directory, "repositories", repo_name)

    repo_dir = os.path.join(repo_cwd, "repository")
    repo_url = get_repo_url(args, item.attributes)
    if not repo_url:
        logger.error("Could not determine repository URL for {0}".format(repo_name))
        return
    fetch_repository(
        args,
        repo_name,
        repo_url,
        repo_dir,
        skip_existing=args.skip_existing,
        bare_clone=args.clone_bare,
        lfs_clone=args.clone_lfs,
    )


def get_repo_url(args, attributes):
    if args.prefer_ssh:
        return attributes.get("ssh_url_to_repo", None)

    return attributes.get("http_url_to_repo", None)


def get_client(args):
    if not args.host:
        logger.error("Missing --host flag")
        return None

    if args.disable_ssl_verification:
        # Only silence urllib3 when the user asked for unverified TLS, so a
        # genuine certificate problem is still visible by default
        urllib3.disable_warnings()

    client = None
    if args.private_token:
        args.private_token = read_token(args.private_token)

        client = gitlab.Gitlab(
            args.host,
            private_token=args.private_token,
            ssl_verify=not args.disable_ssl_verification,
        )
    elif args.oauth_token:
        args.oauth_token = read_token(args.oauth_token)

        client = gitlab.Gitlab(
            args.host,
            oauth_token=args.oauth_token,
            ssl_verify=not args.disable_ssl_verification,
        )
    elif args.username:
        raise Exception(
            "--username and --password are no longer usable: GitLab removed "
            "password authentication from its API, and python-gitlab dropped "
            "support for it in 3.0. Create a personal access token with the "
            "read_api and read_repository scopes and pass it with "
            "--private-token instead."
        )
    else:
        client = gitlab.Gitlab(args.host, ssl_verify=not args.disable_ssl_verification)

    return client


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Backup a gitlab account")
    parser.add_argument("--host", dest="host", help="gitlab host")
    # Hidden rather than removed: GitLab dropped password authentication, but
    # an existing invocation should get the actionable error from get_client
    # instead of an "unrecognized arguments" failure
    parser.add_argument("--username", dest="username", help=argparse.SUPPRESS)
    parser.add_argument("--password", dest="password", help=argparse.SUPPRESS)
    parser.add_argument(
        "--oauth-token",
        dest="oauth_token",
        help="oauth token, or path to token (file://...)",
    )
    parser.add_argument(
        "--private-token",
        dest="private_token",
        help="private token, or path to token (file://...)",
    )
    parser.add_argument(
        "--clone-bare",
        action="store_true",
        dest="clone_bare",
        help="clone bare repositories",
    )
    parser.add_argument(
        "--clone-lfs",
        action="store_true",
        dest="clone_lfs",
        help="clone LFS repositories (requires Git LFS to be installed, https://git-lfs.github.com)",
    )
    parser.add_argument(
        "--disable-ssl-verification",
        action="store_true",
        dest="disable_ssl_verification",
        help="disable ssl verification",
    )
    parser.add_argument(
        "--namespace",
        default=None,
        dest="namespace",
        help="specify a gitlab namespace to backup, including its subgroups",
    )
    parser.add_argument(
        "--output-directory",
        default=".",
        dest="output_directory",
        help="directory at which to backup the repositories",
    )
    parser.add_argument(
        "--prefer-ssh",
        action="store_true",
        dest="prefer_ssh",
        help="Clone repositories using SSH instead of HTTPS",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        dest="skip_existing",
        help="skip project if a backup directory exists",
    )
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument(
        "--owned-only",
        action="store_true",
        dest="owned_only",
        help="only backup projects owned by the provided user or key",
    )
    scope.add_argument(
        "--with-membership",
        action="store_true",
        dest="with_membership",
        help="backup projects the provided user or key is a member of " "(the default)",
    )
    scope.add_argument(
        "--all-visible",
        action="store_true",
        dest="all_visible",
        help="backup every project the token can see, including public ones "
        "it is not a member of. On a large instance such as gitlab.com this "
        "enumerates millions of projects and will not finish",
    )
    parser.add_argument(
        "--private_key", default="", dest="private_key", help="Path to the private key"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        dest="quiet",
        help="only log warnings and errors",
    )
    parser.add_argument(
        "--allow-host-change",
        action="store_true",
        dest="allow_host_change",
        help="permit an existing clone's origin to move to a different host, "
        "for when the gitlab instance was renamed",
    )
    parser.add_argument(
        "--git-timeout",
        type=non_negative_int,
        default=0,
        dest="git_timeout",
        help="abandon a single git command after this many seconds (0 disables)",
    )
    parser.add_argument(
        "--stall-timeout",
        type=non_negative_int,
        default=60,
        dest="stall_timeout",
        help="abandon an http transfer that makes no progress for this many "
        "seconds (0 disables)",
    )
    parser.add_argument(
        "--retries",
        type=non_negative_int,
        default=3,
        dest="retries",
        help="how many times to retry a failed git command",
    )
    parser.add_argument(
        "--log-level",
        default=None,
        dest="log_level",
        help="log level to use (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    return parser.parse_args(args)
