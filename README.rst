=============
gitlab-backup
=============

|PyPI| |Python Versions|

backup a gitlab user or organization

Requirements
============

- GIT 2.31+ (credentials are passed via ``GIT_CONFIG_*`` so they never appear
  in ``ps`` output)
- Git LFS, only when using ``--clone-lfs``

Installation
============

Using PIP via PyPI::

    pip install gitlab-backup

Using PIP via Github::

    pip install git+https://github.com/josegonzalez/python-gitlab-backup.git#egg=gitlab-backup

Usage
=====

CLI Usage is as follows::

    usage: gitlab-backup [-h] [--version] [--host HOST]
                         [--oauth-token OAUTH_TOKEN]
                         [--private-token PRIVATE_TOKEN] [--clone-bare]
                         [--clone-lfs] [--disable-ssl-verification]
                         [--namespace NAMESPACE]
                         [--output-directory OUTPUT_DIRECTORY] [--prefer-ssh]
                         [--skip-existing] [--owned-only | --with-membership |
                         --all-visible] [--private-key PRIVATE_KEY] [--quiet]
                         [--allow-host-change] [--api-timeout API_TIMEOUT]
                         [--git-timeout GIT_TIMEOUT]
                         [--stall-timeout STALL_TIMEOUT] [--retries RETRIES]
                         [--log-level LOG_LEVEL]

    Backup a gitlab account

    options:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      --host HOST           gitlab host
      --oauth-token OAUTH_TOKEN
                            oauth token, or path to token (file://...)
      --private-token PRIVATE_TOKEN
                            private token, or path to token (file://...)
      --clone-bare          clone bare repositories
      --clone-lfs           clone LFS repositories (requires Git LFS to be
                            installed, https://git-lfs.github.com)
      --disable-ssl-verification
                            disable ssl verification
      --namespace NAMESPACE
                            specify a gitlab namespace to backup, including its
                            subgroups
      --output-directory OUTPUT_DIRECTORY
                            directory at which to backup the repositories
      --prefer-ssh          Clone repositories using SSH instead of HTTPS
      --skip-existing       skip project if a backup directory exists
      --owned-only          only backup projects owned by the provided user or key
      --with-membership     backup projects the provided user or key is a member
                            of (the default)
      --all-visible         backup every project the token can see, including
                            public ones it is not a member of. On a large instance
                            such as gitlab.com this enumerates millions of
                            projects and will not finish
      --private-key, --private_key PRIVATE_KEY
                            Path to the private key
      --quiet               only log warnings and errors
      --allow-host-change   permit an existing clone's origin to move to a
                            different host, for when the gitlab instance was
                            renamed
      --api-timeout API_TIMEOUT
                            abandon a gitlab api request after this many seconds
                            (0 disables)
      --git-timeout GIT_TIMEOUT
                            abandon a single git command after this many seconds
                            (0 disables)
      --stall-timeout STALL_TIMEOUT
                            abandon an http transfer that makes no progress for
                            this many seconds (0 disables)
      --retries RETRIES     how many times to retry a failed git command
      --log-level LOG_LEVEL
                            log level to use (DEBUG, INFO, WARNING, ERROR,
                            CRITICAL)

It can also be run as a module::

    python -m gitlab_backup --help


.. |PyPI| image:: https://img.shields.io/pypi/v/gitlab-backup.svg
   :target: https://pypi.python.org/pypi/gitlab-backup/
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/gitlab-backup.svg
   :target: https://github.com/albertyw/gitlab-backup
