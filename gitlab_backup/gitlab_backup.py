#!/usr/bin/env python

import argparse
import base64
import getpass
import logging
import os
import subprocess
import sys
import threading

import gitlab
import urllib3

from urllib.parse import urlparse, urlunparse

logger = logging.getLogger(__name__)

SECRET = "*****"

FILE_URI_PREFIX = "file://"


class GitCommandError(Exception):
    """Raised when a git subprocess exits non-zero."""


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
    popenargs, stdout_log_level=logging.DEBUG, stderr_log_level=logging.ERROR, **kwargs
):
    """
    Variant of subprocess.call that accepts a logger instead of stdout/stderr,
    and logs stdout messages via logger.debug and stderr messages via
    logger.error.
    """
    child = subprocess.Popen(
        popenargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs
    )

    def log_output(pipe, log_level):
        # Drain the pipe from a thread so the child never blocks on a full
        # pipe buffer, logging each line as it arrives.
        with pipe:
            for line in iter(pipe.readline, b""):
                try:
                    logger.log(log_level, line.rstrip(b"\r\n"))
                except Exception:
                    # Keep draining even if logging fails, or the child
                    # blocks on a full pipe buffer again
                    pass

    threads = [
        threading.Thread(
            target=log_output, args=(child.stdout, stdout_log_level), daemon=True
        ),
        threading.Thread(
            target=log_output, args=(child.stderr, stderr_log_level), daemon=True
        ),
    ]
    for thread in threads:
        thread.start()

    rc = child.wait()

    # Timeout in case a grandchild inherited the pipe handles and keeps
    # them open past the child's exit, which would delay EOF indefinitely
    for thread in threads:
        thread.join(timeout=60)

    if rc != 0:
        print("{} returned {}:".format(popenargs[0], rc), file=sys.stderr)
        print("\t", " ".join(mask_command(popenargs)), file=sys.stderr)

    return rc


def run_git(popenargs, **kwargs):
    """Run a git command, raising GitCommandError if it fails.

    Every git failure has to surface: a backup that silently skipped half its
    repositories is worse than one that reports an error.
    """
    rc = logging_subprocess(popenargs, **kwargs)
    if rc != 0:
        raise GitCommandError(
            "{0} exited with code {1}".format(" ".join(mask_command(popenargs)), rc)
        )
    return rc


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
    full_path = attributes["namespace"]["full_path"]
    if args.namespace and args.namespace != full_path:
        logger.debug(
            "Skipping {0} as namespace does not match {1}".format(
                attributes["path_with_namespace"], args.namespace
            )
        )
        return False
    return True


def get_git_env(args):
    """Build the environment for git subprocesses.

    The credential travels in GIT_CONFIG_* rather than on the command line so
    it does not appear in `ps` output. Requires git 2.31+.
    """
    env = os.environ.copy()

    token = read_token(args.private_token or args.oauth_token)
    if not token:
        return env

    auth_pair = "oauth2:{0}".format(token).encode("utf-8")
    b64_auth = base64.b64encode(auth_pair).decode("utf-8")

    try:
        count = int(env.get("GIT_CONFIG_COUNT", "0"))
    except ValueError:
        count = 0

    env["GIT_CONFIG_KEY_{0}".format(count)] = "http.extraHeader"
    env["GIT_CONFIG_VALUE_{0}".format(count)] = "Authorization: Basic {0}".format(
        b64_auth
    )
    env["GIT_CONFIG_COUNT"] = str(count + 1)
    return env


def check_git_lfs_install():
    exit_code = subprocess.call(
        ["git", "lfs", "version"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if exit_code != 0:
        raise Exception(
            "The argument --clone-lfs requires you to have Git LFS installed.\n"
            "You can get it from https://git-lfs.github.com."
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

    if bare_clone:
        if os.path.exists(local_dir):
            clone_exists = (
                subprocess.check_output(
                    ["git", "rev-parse", "--is-bare-repository"],
                    cwd=local_dir,
                    env=git_env,
                )
                == b"true\n"
            )
        else:
            clone_exists = False
    else:
        clone_exists = os.path.exists(os.path.join(local_dir, ".git"))

    if clone_exists and skip_existing:
        return

    masked_remote_url = mask_password(remote_url)

    # An empty-but-existing repository answers ls-remote with an exit code of 0
    # and no refs, so a non-zero code always means the remote could not be read
    initialized = subprocess.call(
        ["git", "ls-remote", remote_url],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=git_env,
    )
    if initialized != 0:
        raise GitCommandError(
            "Could not read {0} ({1}): git ls-remote exited with code {2}. "
            "The repository may be missing, private, or the credentials may be "
            "invalid".format(name, masked_remote_url, initialized)
        )

    if clone_exists:
        logger.info("Updating {0} in {1}".format(name, local_dir))

        remotes = subprocess.check_output(
            ["git", "remote", "show"], cwd=local_dir, env=git_env
        )
        remotes = [i.strip() for i in remotes.decode("utf-8").splitlines()]

        if "origin" not in remotes:
            git_command = ["git", "remote", "add", "origin", remote_url]
            run_git(git_command, cwd=local_dir, env=git_env)
        else:
            git_command = ["git", "remote", "set-url", "origin", remote_url]
            run_git(git_command, cwd=local_dir, env=git_env)

        run_git(
            ["git", "fetch", "--all", "--force", "--tags", "--prune"],
            cwd=local_dir,
            env=git_env,
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
        run_git(git_command, env=git_env)

    # LFS objects are fetched in addition to the refs above, never instead of
    # them, otherwise a --clone-lfs backup would stop receiving new commits
    if lfs_clone:
        run_git(["git", "lfs", "fetch", "--all", "--prune"], cwd=local_dir, env=git_env)


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
        if not args.password:
            args.password = getpass.getpass()

        if not args.password:
            raise Exception("You must specify a password for basic auth")

        client = gitlab.Gitlab(
            args.host,
            email=args.username,
            password=args.password,
            ssl_verify=not args.disable_ssl_verification,
        )
        client.auth()
    else:
        client = gitlab.Gitlab(args.host, ssl_verify=not args.disable_ssl_verification)

    return client


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Backup a gitlab account")
    parser.add_argument("--host", dest="host", help="gitlab host")
    parser.add_argument("--username", dest="username", help="username for basic auth")
    parser.add_argument(
        "--password",
        dest="password",
        help="password for basic auth. "
        "If a username is given but not a password, the "
        "password will be prompted for.",
    )
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
        help="specify a gitlab namespace to backup",
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
    parser.add_argument(
        "--owned-only",
        action="store_true",
        dest="owned_only",
        help="Only backup projects owned by the provided user or key",
    )
    parser.add_argument(
        "--with-membership",
        action="store_true",
        dest="with_membership",
        help="Backup projects provided user or key is member of",
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
        "--log-level",
        default=None,
        dest="log_level",
        help="log level to use (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    return parser.parse_args(args)
