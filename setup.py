#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from gitlab_backup import __version__

try:
    from setuptools import setup

    setup  # workaround for pyflakes issue #13
except ImportError:
    from distutils.core import setup

# Hack to prevent stupid TypeError: 'NoneType' object is not callable error on
# exit of python setup.py test # in multiprocessing/util.py _exit_function when
# running python setup.py test (see
# http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html)
try:
    import multiprocessing

    multiprocessing
except ImportError:
    pass


def read_file(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name="gitlab-backup",
    version=__version__,
    author="Jose Diaz-Gonzalez",
    author_email="gitlab-backup@josediazgonzalez.com",
    packages=["gitlab_backup"],
    entry_points={
        "console_scripts": [
            "gitlab-backup=gitlab_backup.cli:run",
        ],
    },
    url="http://github.com/josegonzalez/python-gitlab-backup",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: System :: Archiving :: Backup",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
    description="backup a gitlab user or organization",
    long_description=read_file("README.rst"),
    long_description_content_type="text/x-rst",
    install_requires=read_file("requirements.txt").splitlines(),
    python_requires=">=3.10",
    zip_safe=True,
)
