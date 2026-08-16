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

from urllib.parse import urlparse

urllib3.disable_warnings()

logger = logging.getLogger(__name__)


class GitCommandError(Exception):
    """Raised when a git subprocess exits non-zero."""


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
        print("\t", " ".join(popenargs), file=sys.stderr)

    return rc


def run_git(popenargs, **kwargs):
    """Run a git command, raising GitCommandError if it fails.

    Every git failure has to surface: a backup that silently skipped half its
    repositories is worse than one that reports an error.
    """
    rc = logging_subprocess(popenargs, **kwargs)
    if rc != 0:
        raise GitCommandError(
            "{0} exited with code {1}".format(" ".join(popenargs), rc)
        )
    return rc


def mkdir_p(*args):
    for path in args:
        os.makedirs(path, exist_ok=True)


def mask_password(url, secret="*****"):
    parsed = urlparse(url)

    if not parsed.password:
        return url
    elif parsed.password == "x-oauth-basic":
        return url.replace(parsed.username, secret)

    return url.replace(parsed.password, secret)


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


def get_git_extra_args(args):
    if args.private_token:
        auth_pair = "oauth2:{0}".format(args.private_token).encode("utf-8")
        b64_auth = base64.b64encode(auth_pair).decode("utf-8")
        return ["-c", "http.extraHeader=Authorization: Basic {0}".format(b64_auth)]
    elif args.oauth_token:
        auth_pair = "oauth2:{0}".format(args.oauth_token).encode("utf-8")
        b64_auth = base64.b64encode(auth_pair).decode("utf-8")
        return ["-c", "http.extraHeader=Authorization: Basic {0}".format(b64_auth)]
    return []


def fetch_repository(
    args,
    name,
    remote_url,
    local_dir,
    skip_existing=False,
    bare_clone=False,
    lfs_clone=False,
):
    if bare_clone:
        if os.path.exists(local_dir):
            clone_exists = (
                subprocess.check_output(
                    ["git", "rev-parse", "--is-bare-repository"], cwd=local_dir
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
    extra_args = get_git_extra_args(args)

    ls_remote_cmd = ["git"] + extra_args + ["ls-remote", remote_url]
    # An empty-but-existing repository answers ls-remote with an exit code of 0
    # and no refs, so a non-zero code always means the remote could not be read
    initialized = subprocess.call(
        ls_remote_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    if initialized != 0:
        raise GitCommandError(
            "Could not read {0} ({1}): git ls-remote exited with code {2}. "
            "The repository may be missing, private, or the credentials may be "
            "invalid".format(name, masked_remote_url, initialized)
        )

    if clone_exists:
        logger.info("Updating {0} in {1}".format(name, local_dir))

        remotes = subprocess.check_output(["git", "remote", "show"], cwd=local_dir)
        remotes = [i.strip() for i in remotes.decode("utf-8").splitlines()]

        if "origin" not in remotes:
            git_command = ["git"] + extra_args + ["remote", "add", "origin", remote_url]
            run_git(git_command, cwd=local_dir)
        else:
            git_command = (
                ["git"] + extra_args + ["remote", "set-url", "origin", remote_url]
            )
            run_git(git_command, cwd=local_dir)

        if lfs_clone:
            git_command = (
                [
                    "git",
                ]
                + extra_args
                + [
                    "lfs",
                    "fetch",
                    "--all",
                    "--prune",
                ]
            )
        else:
            git_command = (
                ["git"]
                + extra_args
                + ["fetch", "--all", "--force", "--tags", "--prune"]
            )
        run_git(git_command, cwd=local_dir)
    else:
        logger.info(
            "Cloning {0} repository from {1} to {2}".format(
                name, masked_remote_url, local_dir
            )
        )
        if bare_clone:
            git_command = (
                ["git"] + extra_args + ["clone", "--mirror", remote_url, local_dir]
            )
        else:
            git_command = ["git"] + extra_args + ["clone", remote_url, local_dir]
        run_git(git_command)


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

    _path_specifier = "file://"

    client = None
    if args.private_token:
        if args.private_token.startswith(_path_specifier):
            filename = args.private_token[len(_path_specifier) :]
            with open(filename, "rt") as f:
                args.private_token = f.readline().strip()

        client = gitlab.Gitlab(
            args.host,
            private_token=args.private_token,
            ssl_verify=not args.disable_ssl_verification,
        )
    elif args.oauth_token:
        if args.oauth_token.startswith(_path_specifier):
            filename = args.oauth_token[len(_path_specifier) :]
            with open(filename, "rt") as f:
                args.oauth_token = f.readline().strip()

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
