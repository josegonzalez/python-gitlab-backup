#!/usr/bin/env python
"""Command-line interface for gitlab-backup."""

import collections
import logging
import os
import sys
import tempfile

from gitlab_backup.gitlab_backup import (
    backup_repository,
    check_git_install,
    check_git_lfs_install,
    get_client,
    logger,
    mkdir_p,
    parse_args,
    should_include_repository,
)


def filesystem_is_case_insensitive(path):
    """Whether two names differing only in case are one file here.

    Probed rather than assumed: on ext4 two projects whose paths differ only in
    capitalisation are distinct directories and both back up correctly, so the
    collision check must not fire there.
    """
    try:
        handle, probe = tempfile.mkstemp(prefix="GitlabBackupCaseProbe", dir=path)
        os.close(handle)
    except OSError:
        # Cannot tell, so assume the riskier filesystem
        return True

    try:
        directory, name = os.path.split(probe)
        return name != name.lower() and os.path.exists(
            os.path.join(directory, name.lower())
        )
    finally:
        try:
            os.unlink(probe)
        except OSError:
            # A scanner or indexer holding the probe must not fail the backup
            logger.debug("Could not remove case probe {0}".format(probe))


def find_colliding_paths(repositories):
    """Group project paths that differ only in capitalisation."""
    by_folded = collections.OrderedDict()
    for path in repositories:
        by_folded.setdefault(path.casefold(), []).append(path)

    return [sorted(group) for group in by_folded.values() if len(group) > 1]


def configure_logging():
    """Install the CLI's handlers.

    Done on demand rather than at import time so that importing this module
    does not reconfigure logging for an embedding application.
    """
    # INFO and DEBUG go to stdout, WARNING and above go to stderr
    log_format = logging.Formatter(
        fmt="%(asctime)s.%(msecs)03d: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.addFilter(lambda r: r.levelno < logging.WARNING)
    stdout_handler.setFormatter(log_format)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.WARNING)
    stderr_handler.setFormatter(log_format)

    logging.basicConfig(level=logging.INFO, handlers=[stdout_handler, stderr_handler])


def main():
    """Main entry point for gitlab-backup CLI."""
    configure_logging()
    args = parse_args()

    # Both switches drive the same logger, so an explicit --log-level wins
    # over --quiet rather than being silently swallowed by it
    if args.quiet:
        logger.root.setLevel(logging.WARNING)

    if args.log_level:
        log_level = logging.getLevelName(args.log_level.upper())
        if isinstance(log_level, int):
            logger.root.setLevel(log_level)
        else:
            raise Exception("Unknown --log-level {0}".format(args.log_level))

    check_git_install()

    if args.clone_lfs:
        check_git_lfs_install()

    if args.private_key != "":
        logger.info("Use the private key: {0}".format(args.private_key))
        os.environ["GIT_SSH_COMMAND"] = 'ssh -i "{0}" -o IdentitiesOnly=yes'.format(
            args.private_key
        )

    client = get_client(args)
    if not client:
        raise Exception("Unable to create gitlab client")

    # Resolve once and write it back, so the directory that gets created and
    # the one repositories are cloned into can never drift apart
    output_directory = os.path.realpath(args.output_directory)
    args.output_directory = output_directory
    if not os.path.isdir(output_directory):
        logger.info("Create output directory {0}".format(output_directory))
        mkdir_p(output_directory)

    # Default to the projects the user is a member of. Asking for everything
    # the token can see means every public project on the instance, which on
    # gitlab.com is millions and looks indistinguishable from a hang.
    owned = args.owned_only
    membership = args.with_membership
    if not (owned or membership or args.all_visible):
        membership = True

    if args.all_visible:
        logger.info("Listing every project visible to this token")
    elif owned:
        logger.info("Listing projects owned by this user")
    else:
        logger.info("Listing projects this user is a member of")

    items = client.projects.list(get_all=True, owned=owned, membership=membership)
    repositories = {}
    unreadable = []
    for item in items:
        # Filter before checking for collisions, so projects this run is not
        # backing up cannot fail it
        path = getattr(item, "path_with_namespace", None)
        if not path or not isinstance(path, str):
            logger.error("Skipping a project with no usable path: {0!r}".format(path))
            unreadable.append("<project with no path>")
            continue

        try:
            if not should_include_repository(args, item.attributes):
                continue
        except Exception as e:
            # One unexpected project must cost only itself, not the backup
            logger.error("Could not read project {0}: {1}".format(path or item, e))
            unreadable.append(path or str(item))
            continue
        repositories[path] = item

    repositories = collections.OrderedDict(sorted(repositories.items()))

    # One unreachable or broken repository must not cost you the other 200,
    # but it still has to make the run exit non-zero
    # Two projects whose paths differ only in capitalisation share a directory
    # on a case-insensitive filesystem. Report them instead of letting the
    # second quietly fetch over the first.
    colliding = (
        find_colliding_paths(repositories)
        if filesystem_is_case_insensitive(output_directory)
        else []
    )
    for group in colliding:
        logger.error(
            "These projects share one directory on a case-insensitive "
            "filesystem and cannot both be backed up here: {0}".format(", ".join(group))
        )

    failed = unreadable + [path for group in colliding for path in group]
    for path, item in repositories.items():
        if path in failed:
            continue
        try:
            backup_repository(args, item)
        except Exception as e:
            logger.error("Failed to back up {0}: {1}".format(path, e))
            failed.append(path)

    if failed:
        raise Exception(
            "{0} of {1} repositories failed to back up: {2}".format(
                len(failed), len(repositories) + len(unreadable), ", ".join(failed)
            )
        )


def run():
    """Console script entry point.

    Reports failures as a single error line and a non-zero exit status rather
    than an unhandled traceback.
    """
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("Interrupted")
        sys.exit(130)
    except Exception as e:
        logger.error(str(e))
        sys.exit(1)


if __name__ == "__main__":
    run()
