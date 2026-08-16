"""Tests for backup_repository, the per-project entry point."""

import logging
import os
from unittest.mock import patch

import pytest

from gitlab_backup.gitlab_backup import backup_repository


class Project:
    """Stand-in for a python-gitlab Project object."""

    def __init__(self, **overrides):
        self.attributes = {
            "namespace": {"full_path": "group"},
            "path_with_namespace": "group/project",
            "http_url_to_repo": "https://gitlab.example.com/group/project.git",
            "ssh_url_to_repo": "git@gitlab.example.com:group/project.git",
        }
        self.attributes.update(overrides)

    @property
    def path_with_namespace(self):
        return self.attributes["path_with_namespace"]


@pytest.fixture
def fetch():
    with patch("gitlab_backup.gitlab_backup.fetch_repository") as mock_fetch:
        yield mock_fetch


class TestBackupRepository:
    def test_clones_into_repositories_subdirectory(self, create_args, fetch, tmp_path):
        args = create_args(output_directory=str(tmp_path))

        backup_repository(args, Project())

        args_passed = fetch.call_args.args
        assert args_passed[1] == "group/project"
        assert args_passed[2] == "https://gitlab.example.com/group/project.git"
        assert args_passed[3] == os.path.join(
            str(tmp_path), "repositories", "group/project", "repository"
        )

    def test_clone_options_are_forwarded(self, create_args, fetch, tmp_path):
        args = create_args(
            output_directory=str(tmp_path),
            skip_existing=True,
            clone_bare=True,
            clone_lfs=True,
        )

        backup_repository(args, Project())

        assert fetch.call_args.kwargs == {
            "skip_existing": True,
            "bare_clone": True,
            "lfs_clone": True,
        }

    def test_prefer_ssh_selects_the_ssh_url(self, create_args, fetch, tmp_path):
        args = create_args(output_directory=str(tmp_path), prefer_ssh=True)

        backup_repository(args, Project())

        assert fetch.call_args.args[2] == "git@gitlab.example.com:group/project.git"

    def test_namespace_mismatch_short_circuits(self, create_args, fetch, tmp_path):
        args = create_args(output_directory=str(tmp_path), namespace="other")

        backup_repository(args, Project())

        fetch.assert_not_called()

    def test_missing_repo_url_logs_and_returns(
        self, create_args, fetch, tmp_path, caplog
    ):
        args = create_args(output_directory=str(tmp_path))
        project = Project()
        del project.attributes["http_url_to_repo"]

        with caplog.at_level(logging.ERROR, logger="gitlab_backup.gitlab_backup"):
            backup_repository(args, project)

        fetch.assert_not_called()
        assert "Could not determine repository URL for group/project" in caplog.text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
