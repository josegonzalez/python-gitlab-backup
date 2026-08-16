#!/usr/bin/env python
"""Command-line interface for gitlab-backup."""

import collections
import logging
import os
import sys

from gitlab_backup.gitlab_backup import (
    backup_repository,
    get_client,
    logger,
    mkdir_p,
    parse_args,
)

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
    args = parse_args()

    if args.quiet:
        logger.setLevel(logging.WARNING)

    if args.log_level:
        log_level = logging.getLevelName(args.log_level.upper())
        if isinstance(log_level, int):
            logger.root.setLevel(log_level)

    if args.private_key != "":
        logger.info("Use the private key: {0}".format(args.private_key))
        os.environ["GIT_SSH_COMMAND"] = 'ssh -i "{0}" -o IdentitiesOnly=yes'.format(
            args.private_key
        )

    client = get_client(args)
    if not client:
        raise Exception("Unable to create gitlab client")

    output_directory = os.path.realpath(args.output_directory)
    if not os.path.isdir(output_directory):
        logger.info("Create output directory {0}".format(output_directory))
        mkdir_p(output_directory)

    items = client.projects.list(
        get_all=True, owned=args.owned_only, membership=args.with_membership
    )
    repositories = {}
    for item in items:
        repositories[item.path_with_namespace] = item

    repositories = collections.OrderedDict(sorted(repositories.items()))
    for path, item in repositories.items():
        backup_repository(args, item)


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
