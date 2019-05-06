=============
gitlab-backup
=============

|PyPI| |Python Versions|

backup a gitlab user or organization

Requirements
============

- GIT 1.9+

Installation
============

Using PIP via PyPI::

    pip install gitlab-backup

Using PIP via Github::

    pip install git+https://github.com/josegonzalez/python-gitlab-backup.git#egg=gitlab-backup

Usage
=====

CLI Usage is as follows::

    usage: gitlab-backup [-h] [--host HOST] [--username USERNAME]
                         [--password PASSWORD] [--oath-token OATH_TOKEN]
                         [--private-token PRIVATE_TOKEN] [--clone-bare]
                         [--clone-lfs] [--disable-ssl-verification]
                         [--namespace NAMESPACE]
                         [--output-directory OUTPUT_DIRECTORY] [--prefer-ssh]
                         [--skip-existing]

    Backup a gitlab account

    optional arguments:
      -h, --help            show this help message and exit
      --host HOST           gitlab host
      --username USERNAME   username for basic auth
      --password PASSWORD   password for basic auth. If a username is given but
                            not a password, the password will be prompted for.
      --oath-token OATH_TOKEN
                            oath token, or path to token (file://...)
      --private-token PRIVATE_TOKEN
                            private token, or path to token (file://...)
      --clone-bare          clone bare repositories
      --clone-lfs           clone LFS repositories (requires Git LFS to be
                            installed, https://git-lfs.github.com)
      --disable-ssl-verification
                            disable ssl verification
      --namespace NAMESPACE
                            specify a gitlab namespace to backup
      --output-directory OUTPUT_DIRECTORY
                            directory at which to backup the repositories
      --prefer-ssh          Clone repositories using SSH instead of HTTPS
      --skip-existing       skip project if a backup directory exists
      --with-membership     Backup projects provided user or key is member of


.. |PyPI| image:: https://img.shields.io/pypi/v/gitlab-backup.svg
   :target: https://pypi.python.org/pypi/gitlab-backup/
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/gitlab-backup.svg
   :target: https://github.com/albertyw/gitlab-backup
