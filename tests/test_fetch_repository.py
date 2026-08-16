"""Tests for fetch_repository clone and update flows."""

from unittest.mock import patch

import pytest

from gitlab_backup.gitlab_backup import GitCommandError, fetch_repository

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
            self.rc_by_subcommand = {}

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

        def _logging_subprocess(self, popenargs, **kwargs):
            for subcommand, rc in self.rc_by_subcommand.items():
                if subcommand in popenargs:
                    return rc
            return 0

    helper = Git()
    with patch("gitlab_backup.gitlab_backup.time.sleep"), patch(
        "gitlab_backup.gitlab_backup.probe_remote",
        side_effect=lambda *a, **kw: helper.ls_remote_rc,
    ) as mock_probe, patch(
        "gitlab_backup.gitlab_backup.subprocess.check_output",
        side_effect=helper._check_output,
    ) as mock_check_output, patch(
        "gitlab_backup.gitlab_backup.logging_subprocess",
        side_effect=helper._logging_subprocess,
    ) as mock_logging_subprocess:
        helper.probe = mock_probe
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

    def test_lfs_objects_are_fetched_after_a_first_clone(self, create_args, git):
        """Without this, LFS content is missing until the next run."""
        args = create_args()

        fetch_repository(
            args, "group/project", REMOTE_URL, git.local_dir, lfs_clone=True
        )

        assert git.commands == [
            ["git", "clone", REMOTE_URL, git.local_dir],
            ["git", "lfs", "fetch", "--all", "--prune"],
        ]

    def test_credentials_never_reach_the_command_line(self, create_args, git):
        args = create_args(private_token="glpat-secret")

        fetch_repository(args, "group/project", REMOTE_URL, git.local_dir)

        for command in git.commands:
            assert not any("glpat-secret" in arg for arg in command)
            assert "-c" not in command

    def test_credentials_are_passed_through_the_environment(self, create_args, git):
        args = create_args(private_token="glpat-secret")

        fetch_repository(args, "group/project", REMOTE_URL, git.local_dir)

        env = git.logging_subprocess.call_args.kwargs["env"]
        assert env["GIT_CONFIG_KEY_0"] == "http.extraHeader"

    def test_ls_remote_also_uses_the_authenticated_environment(self, create_args, git):
        args = create_args(private_token="glpat-secret")

        fetch_repository(args, "group/project", REMOTE_URL, git.local_dir)

        assert git.probe.call_args.args[0] == REMOTE_URL
        assert git.probe.call_args.kwargs["git_env"]["GIT_CONFIG_KEY_0"] == (
            "http.extraHeader"
        )

    def test_skip_existing_does_not_skip_a_missing_clone(self, create_args, git):
        args = create_args()

        fetch_repository(
            args, "group/project", REMOTE_URL, git.local_dir, skip_existing=True
        )

        assert git.commands

    def test_failed_clone_raises(self, create_args, git):
        args = create_args()
        git.rc_by_subcommand = {"clone": 128}

        with pytest.raises(GitCommandError) as exc_info:
            fetch_repository(args, "group/project", REMOTE_URL, git.local_dir)

        assert "exited with code 128" in str(exc_info.value)


class TestUnreachableRepository:
    """git ls-remote answers 0 for an empty-but-existing repository, so any
    non-zero code means the remote could not be read at all. Treating 128 as
    "not initialized" used to hide bad credentials behind a silent skip."""

    @pytest.mark.parametrize("rc", [1, 128])
    def test_unreachable_remote_raises(self, create_args, git, rc):
        args = create_args()
        git.ls_remote_rc = rc

        with pytest.raises(GitCommandError) as exc_info:
            fetch_repository(args, "group/project", REMOTE_URL, git.local_dir)

        assert "Could not read group/project" in str(exc_info.value)
        assert git.commands == []

    def test_failure_names_the_likely_causes(self, create_args, git):
        args = create_args()
        git.ls_remote_rc = 128

        with pytest.raises(GitCommandError) as exc_info:
            fetch_repository(args, "group/project", REMOTE_URL, git.local_dir)

        assert "missing, private, or the credentials may be invalid" in str(
            exc_info.value
        )

    def test_masked_url_is_used_in_failure_messages(self, create_args, git):
        args = create_args()
        git.ls_remote_rc = 128
        remote_url = "https://someone:hunter2@gitlab.example.com/group/project.git"

        with pytest.raises(GitCommandError) as exc_info:
            fetch_repository(args, "group/project", remote_url, git.local_dir)

        assert "hunter2" not in str(exc_info.value)


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

    def test_lfs_clone_still_fetches_refs(self, create_args, git):
        """Regression: --clone-lfs used to replace the ref fetch entirely, so
        backups stopped receiving new commits after the first clone."""
        args = create_args()
        git.make_clone()

        fetch_repository(
            args, "group/project", REMOTE_URL, git.local_dir, lfs_clone=True
        )

        assert git.command_containing("fetch", "--tags") is not None
        assert git.command_containing("lfs") == [
            "git",
            "lfs",
            "fetch",
            "--all",
            "--prune",
        ]

    def test_refs_are_fetched_before_lfs_objects(self, create_args, git):
        args = create_args()
        git.make_clone()

        fetch_repository(
            args, "group/project", REMOTE_URL, git.local_dir, lfs_clone=True
        )

        subcommands = [c[1] for c in git.commands]
        assert subcommands.index("fetch") < subcommands.index("lfs")

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
        git.probe.assert_not_called()

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

    def test_failed_fetch_raises(self, create_args, git):
        args = create_args()
        git.make_clone()
        git.rc_by_subcommand = {"fetch": 1}

        with pytest.raises(GitCommandError):
            fetch_repository(args, "group/project", REMOTE_URL, git.local_dir)


class TestRetries:
    """One network blip should not fail an otherwise healthy repository."""

    def test_a_failed_fetch_is_retried(self, create_args, git):
        args = create_args(retries=2)
        git.make_clone()
        attempts = {"n": 0}

        def flaky(popenargs, **kwargs):
            if "fetch" not in popenargs:
                return 0
            attempts["n"] += 1
            return 0 if attempts["n"] > 2 else 1

        git.logging_subprocess.side_effect = flaky

        fetch_repository(args, "group/project", REMOTE_URL, git.local_dir)

        assert attempts["n"] == 3

    def test_retries_are_exhausted_then_it_raises(self, create_args, git):
        args = create_args(retries=2)
        git.make_clone()
        git.rc_by_subcommand = {"fetch": 1}

        with pytest.raises(GitCommandError):
            fetch_repository(args, "group/project", REMOTE_URL, git.local_dir)

        fetches = [c for c in git.commands if "fetch" in c]
        assert len(fetches) == 3

    def test_no_retries_when_disabled(self, create_args, git):
        args = create_args(retries=0)
        git.make_clone()
        git.rc_by_subcommand = {"fetch": 1}

        with pytest.raises(GitCommandError):
            fetch_repository(args, "group/project", REMOTE_URL, git.local_dir)

        assert len([c for c in git.commands if "fetch" in c]) == 1

    def test_a_clone_is_retried_when_the_path_is_clear(self, create_args, git):
        args = create_args(retries=2)
        git.rc_by_subcommand = {"clone": 1}

        with pytest.raises(GitCommandError):
            fetch_repository(args, "group/project", REMOTE_URL, git.local_dir)

        assert len([c for c in git.commands if "clone" in c]) == 3


class TestTimeout:
    @pytest.mark.parametrize(
        "kwargs",
        [
            {},
            {"lfs_clone": True},
            {"bare_clone": True},
            {"bare_clone": True, "lfs_clone": True},
        ],
    )
    def test_timeout_is_passed_to_every_git_command(self, create_args, git, kwargs):
        """Every git invocation, on every path: one that slips through is a
        command that can hang for ever."""
        args = create_args(git_timeout=30)
        git.make_clone(bare=kwargs.get("bare_clone", False))

        fetch_repository(args, "group/project", REMOTE_URL, git.local_dir, **kwargs)

        assert git.logging_subprocess.call_args_list
        for call in git.logging_subprocess.call_args_list:
            assert call.kwargs["timeout"] == 30, call.args[0]
        assert git.probe.call_args.kwargs["timeout"] == 30

    def test_a_failed_lfs_fetch_is_retried(self, create_args, git):
        """Regression: the lfs fetch was the one command left without retries
        or a timeout, so an LFS blip failed the repository outright."""
        args = create_args(retries=2)
        git.make_clone()
        git.rc_by_subcommand = {"lfs": 1}

        with pytest.raises(GitCommandError):
            fetch_repository(
                args, "group/project", REMOTE_URL, git.local_dir, lfs_clone=True
            )

        assert len([c for c in git.commands if "lfs" in c]) == 3


class TestProbeRetries:
    def test_retries_are_passed_to_the_probe(self, create_args, git):
        args = create_args(retries=4)

        fetch_repository(args, "group/project", REMOTE_URL, git.local_dir)

        assert git.probe.call_args.kwargs["retries"] == 4


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
