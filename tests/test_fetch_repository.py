"""Tests for fetch_repository clone and update flows."""

import logging
from unittest.mock import patch

import pytest

from gitlab_backup.gitlab_backup import fetch_repository

REMOTE_URL = "https://gitlab.example.com/group/project.git"


@pytest.fixture
def git(tmp_path):
    """Patch every subprocess entry point fetch_repository uses.

    Yields a helper exposing the git command lines that were run, so tests
    assert on the arguments rather than on call counts.
    """

    class Git:
        def __init__(self):
            self.local_dir = str(tmp_path / "repository")
            self.ls_remote_rc = 0
            self.is_bare = b"true\n"
            self.remotes = b"origin\n"

        def _check_output(self, popenargs, **kwargs):
            if "rev-parse" in popenargs:
                return self.is_bare
            return self.remotes

        @property
        def commands(self):
            return [call.args[0] for call in self.logging_subprocess.call_args_list]

        def command_containing(self, *needles):
            for command in self.commands:
                if all(needle in command for needle in needles):
                    return command
            return None

        def make_clone(self, bare=False):
            """Create an on-disk clone so fetch_repository takes the update path."""
            if bare:
                (tmp_path / "repository").mkdir(parents=True, exist_ok=True)
            else:
                (tmp_path / "repository" / ".git").mkdir(parents=True, exist_ok=True)

    helper = Git()
    with patch(
        "gitlab_backup.gitlab_backup.subprocess.call",
        side_effect=lambda *a, **kw: helper.ls_remote_rc,
    ) as mock_call, patch(
        "gitlab_backup.gitlab_backup.subprocess.check_output",
        side_effect=helper._check_output,
    ) as mock_check_output, patch(
        "gitlab_backup.gitlab_backup.logging_subprocess", return_value=0
    ) as mock_logging_subprocess:
        helper.call = mock_call
        helper.check_output = mock_check_output
        helper.logging_subprocess = mock_logging_subprocess
        yield helper


class TestFreshClone:
    def test_clones_into_local_dir(self, create_args, git):
        args = create_args()

        fetch_repository(args, "group/project", REMOTE_URL, git.local_dir)

        assert git.commands == [["git", "clone", REMOTE_URL, git.local_dir]]

    def test_bare_clone_uses_mirror(self, create_args, git):
        args = create_args()

        fetch_repository(
            args, "group/project", REMOTE_URL, git.local_dir, bare_clone=True
        )

        assert git.commands == [["git", "clone", "--mirror", REMOTE_URL, git.local_dir]]

    def test_lfs_clone_still_performs_a_plain_first_clone(self, create_args, git):
        """A first clone is always plain; LFS objects arrive on the next update."""
        args = create_args()

        fetch_repository(
            args, "group/project", REMOTE_URL, git.local_dir, lfs_clone=True
        )

        assert git.commands == [["git", "clone", REMOTE_URL, git.local_dir]]

    def test_auth_args_are_prepended_to_git(self, create_args, git):
        args = create_args(private_token="glpat-secret")

        fetch_repository(args, "group/project", REMOTE_URL, git.local_dir)

        command = git.commands[0]
        assert command[:2] == ["git", "-c"]
        assert command[2].startswith("http.extraHeader=Authorization: Basic ")

    def test_auth_args_are_used_for_ls_remote(self, create_args, git):
        args = create_args(private_token="glpat-secret")

        fetch_repository(args, "group/project", REMOTE_URL, git.local_dir)

        ls_remote_cmd = git.call.call_args.args[0]
        assert ls_remote_cmd[:2] == ["git", "-c"]
        assert ls_remote_cmd[-2:] == ["ls-remote", REMOTE_URL]

    def test_skip_existing_does_not_skip_a_missing_clone(self, create_args, git):
        args = create_args()

        fetch_repository(
            args, "group/project", REMOTE_URL, git.local_dir, skip_existing=True
        )

        assert git.commands


class TestUninitializedRepository:
    def test_ls_remote_128_skips_the_repository(self, create_args, git, caplog):
        args = create_args()
        git.ls_remote_rc = 128

        with caplog.at_level(logging.INFO, logger="gitlab_backup.gitlab_backup"):
            fetch_repository(args, "group/project", REMOTE_URL, git.local_dir)

        assert git.commands == []
        assert "since it's not initialized" in caplog.text

    def test_masked_url_is_logged(self, create_args, git, caplog):
        args = create_args()
        git.ls_remote_rc = 128
        remote_url = "https://someone:hunter2@gitlab.example.com/group/project.git"

        with caplog.at_level(logging.INFO, logger="gitlab_backup.gitlab_backup"):
            fetch_repository(args, "group/project", remote_url, git.local_dir)

        assert "hunter2" not in caplog.text
        assert "*****" in caplog.text


class TestExistingClone:
    def test_fetches_all_refs(self, create_args, git):
        args = create_args()
        git.make_clone()

        fetch_repository(args, "group/project", REMOTE_URL, git.local_dir)

        assert git.command_containing("fetch") == [
            "git",
            "fetch",
            "--all",
            "--force",
            "--tags",
            "--prune",
        ]

    def test_lfs_clone_fetches_lfs_objects(self, create_args, git):
        args = create_args()
        git.make_clone()

        fetch_repository(
            args, "group/project", REMOTE_URL, git.local_dir, lfs_clone=True
        )

        assert git.command_containing("lfs") == [
            "git",
            "lfs",
            "fetch",
            "--all",
            "--prune",
        ]
        assert git.command_containing("fetch", "--tags") is None

    def test_existing_origin_is_updated(self, create_args, git):
        args = create_args()
        git.make_clone()
        git.remotes = b"origin\nupstream\n"

        fetch_repository(args, "group/project", REMOTE_URL, git.local_dir)

        assert git.command_containing("remote") == [
            "git",
            "remote",
            "set-url",
            "origin",
            REMOTE_URL,
        ]

    def test_missing_origin_is_added(self, create_args, git):
        args = create_args()
        git.make_clone()
        git.remotes = b"upstream\n"

        fetch_repository(args, "group/project", REMOTE_URL, git.local_dir)

        assert git.command_containing("remote") == [
            "git",
            "remote",
            "add",
            "origin",
            REMOTE_URL,
        ]

    def test_git_runs_in_the_clone_directory(self, create_args, git):
        args = create_args()
        git.make_clone()

        fetch_repository(args, "group/project", REMOTE_URL, git.local_dir)

        for call in git.logging_subprocess.call_args_list:
            assert call.kwargs["cwd"] == git.local_dir

    def test_skip_existing_returns_before_any_git_call(self, create_args, git):
        args = create_args()
        git.make_clone()

        fetch_repository(
            args, "group/project", REMOTE_URL, git.local_dir, skip_existing=True
        )

        assert git.commands == []
        git.call.assert_not_called()

    def test_bare_clone_detected_via_rev_parse(self, create_args, git):
        args = create_args()
        git.make_clone(bare=True)

        fetch_repository(
            args, "group/project", REMOTE_URL, git.local_dir, bare_clone=True
        )

        assert git.command_containing("fetch") is not None

    def test_non_bare_directory_is_recloned_when_bare_requested(self, create_args, git):
        """A directory that is not a bare repo is treated as no clone at all."""
        args = create_args()
        git.make_clone(bare=True)
        git.is_bare = b"false\n"

        fetch_repository(
            args, "group/project", REMOTE_URL, git.local_dir, bare_clone=True
        )

        assert git.commands == [["git", "clone", "--mirror", REMOTE_URL, git.local_dir]]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
