"""Shared pytest fixtures for gitlab-backup tests."""

import pytest

from gitlab_backup.gitlab_backup import parse_args


@pytest.fixture
def create_args():
    """Factory fixture that creates args with real CLI defaults.

    Uses the actual argument parser so new CLI args are automatically
    available with their defaults - no test updates needed.

    Usage:
        def test_something(self, create_args):
            args = create_args(clone_bare=True, host="https://gitlab.com")
    """

    def _create(**overrides):
        # Use real parser to get actual defaults
        args = parse_args([])
        for key, value in overrides.items():
            setattr(args, key, value)
        return args

    return _create
