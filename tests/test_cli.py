"""Tests for the CLI entry point wiring."""

import logging
import os
from unittest.mock import patch

import pytest

from gitlab_backup import cli


def _raise_permission_error(*_args, **_kwargs):
    raise PermissionError(13, "Permission denied")


def project(path):
    """Stand-in for a python-gitlab Project."""
    namespace = path.rsplit("/", 1)[0]
    return type(
        "P",
        (),
        {
            "path_with_namespace": path,
            "attributes": {
                "namespace": {"full_path": namespace},
                "path_with_namespace": path,
                "http_url_to_repo": "https://gitlab.example.com/{0}.git".format(path),
                "ssh_url_to_repo": "git@gitlab.example.com:{0}.git".format(path),
            },
        },
    )()


def client(*paths):
    """Stand-in for a python-gitlab client listing the given projects."""
    projects = [project(p) for p in paths]
    return type(
        "C", (), {"projects": type("L", (), {"list": lambda *a, **kw: projects})()}
    )()


class TestRun:
    """run() is what the console script calls, so it must not leak tracebacks."""

    def test_failure_reports_one_line_and_exits_nonzero(self, caplog):
        with caplog.at_level(logging.ERROR, logger="gitlab_backup.gitlab_backup"):
            with patch.object(cli, "main", side_effect=Exception("boom")):
                with pytest.raises(SystemExit) as exc_info:
                    cli.run()

        assert exc_info.value.code == 1
        assert "boom" in caplog.text

    def test_keyboard_interrupt_exits_130(self, caplog):
        with caplog.at_level(logging.WARNING, logger="gitlab_backup.gitlab_backup"):
            with patch.object(cli, "main", side_effect=KeyboardInterrupt):
                with pytest.raises(SystemExit) as exc_info:
                    cli.run()

        assert exc_info.value.code == 130
        assert "Interrupted" in caplog.text

    def test_success_does_not_exit(self):
        with patch.object(cli, "main", return_value=None):
            cli.run()


class TestMain:
    """main() drives client creation and per-project backup."""

    def test_unusable_client_raises(self, create_args, tmp_path):
        args = create_args(output_directory=str(tmp_path))

        with patch.object(cli, "parse_args", return_value=args), patch.object(
            cli, "get_client", return_value=None
        ):
            with pytest.raises(Exception) as exc_info:
                cli.main()

        assert "Unable to create gitlab client" in str(exc_info.value)

    def test_projects_are_backed_up_in_sorted_order(self, create_args, tmp_path):
        args = create_args(output_directory=str(tmp_path))

        with patch.object(cli, "parse_args", return_value=args), patch.object(
            cli, "get_client", return_value=client("group/zebra", "group/apple")
        ), patch.object(cli, "backup_repository") as mock_backup:
            cli.main()

        backed_up = [
            call.args[1].path_with_namespace for call in mock_backup.call_args_list
        ]
        assert backed_up == ["group/apple", "group/zebra"]

    def test_private_key_sets_git_ssh_command(self, create_args, tmp_path, monkeypatch):
        monkeypatch.delenv("GIT_SSH_COMMAND", raising=False)
        args = create_args(
            output_directory=str(tmp_path), private_key="/home/user/.ssh/id_ed25519"
        )

        with patch.object(cli, "parse_args", return_value=args), patch.object(
            cli, "get_client", return_value=client()
        ):
            cli.main()

        assert os.environ["GIT_SSH_COMMAND"] == (
            'ssh -i "/home/user/.ssh/id_ed25519" -o IdentitiesOnly=yes'
        )

    def test_missing_output_directory_is_created(self, create_args, tmp_path):
        target = tmp_path / "nested" / "backups"
        args = create_args(output_directory=str(target))

        with patch.object(cli, "parse_args", return_value=args), patch.object(
            cli, "get_client", return_value=client()
        ):
            cli.main()

        assert target.is_dir()


class TestFailureIsolation:
    """One broken repository must not cost you the rest of the backup."""

    def test_remaining_repositories_are_still_attempted(self, create_args, tmp_path):
        args = create_args(output_directory=str(tmp_path))
        attempted = []

        def backup(_args, item):
            attempted.append(item.path_with_namespace)
            if item.path_with_namespace == "group/b":
                raise Exception("boom")

        with patch.object(cli, "parse_args", return_value=args), patch.object(
            cli, "get_client", return_value=client("group/a", "group/b", "group/c")
        ), patch.object(cli, "backup_repository", side_effect=backup):
            with pytest.raises(Exception):
                cli.main()

        assert attempted == ["group/a", "group/b", "group/c"]

    def test_failures_are_reported_and_raise(self, create_args, tmp_path, caplog):
        args = create_args(output_directory=str(tmp_path))

        with caplog.at_level(logging.ERROR, logger="gitlab_backup.gitlab_backup"):
            with patch.object(cli, "parse_args", return_value=args), patch.object(
                cli, "get_client", return_value=client("group/a", "group/b")
            ), patch.object(cli, "backup_repository", side_effect=Exception("boom")):
                with pytest.raises(Exception) as exc_info:
                    cli.main()

        assert "2 of 2 repositories failed to back up" in str(exc_info.value)
        assert "group/a" in caplog.text
        assert "boom" in caplog.text

    def test_a_clean_run_does_not_raise(self, create_args, tmp_path):
        args = create_args(output_directory=str(tmp_path))

        with patch.object(cli, "parse_args", return_value=args), patch.object(
            cli, "get_client", return_value=client("group/a")
        ), patch.object(cli, "backup_repository"):
            cli.main()

    def test_failed_run_exits_nonzero(self, create_args, tmp_path):
        """The whole point: cron has to be able to detect a broken backup."""
        args = create_args(output_directory=str(tmp_path))

        with patch.object(cli, "parse_args", return_value=args), patch.object(
            cli, "get_client", return_value=client("group/a")
        ), patch.object(cli, "backup_repository", side_effect=Exception("boom")):
            with pytest.raises(SystemExit) as exc_info:
                cli.run()

        assert exc_info.value.code == 1


class TestLfsPreflight:
    def test_clone_lfs_checks_for_git_lfs(self, create_args, tmp_path):
        args = create_args(output_directory=str(tmp_path), clone_lfs=True)

        with patch.object(cli, "parse_args", return_value=args), patch.object(
            cli, "check_git_lfs_install", side_effect=Exception("no git lfs")
        ) as mock_check:
            with pytest.raises(Exception) as exc_info:
                cli.main()

        mock_check.assert_called_once_with()
        assert "no git lfs" in str(exc_info.value)

    def test_no_check_without_the_flag(self, create_args, tmp_path):
        args = create_args(output_directory=str(tmp_path))

        with patch.object(cli, "parse_args", return_value=args), patch.object(
            cli, "get_client", return_value=client()
        ), patch.object(cli, "check_git_lfs_install") as mock_check:
            cli.main()

        mock_check.assert_not_called()


class TestCaseCollisions:
    """Two projects differing only in capitalisation share one directory on
    macOS and Windows. Backing both up there would merge them.

    The probe is pinned here so these cover the collision logic itself rather
    than the filesystem the tests happen to run on: they would otherwise pass
    on macOS and fail on the ext4 runners in CI."""

    def test_colliding_projects_are_reported_and_skipped(
        self, create_args, tmp_path, caplog
    ):
        args = create_args(output_directory=str(tmp_path))
        attempted = []

        with caplog.at_level(logging.ERROR, logger="gitlab_backup.gitlab_backup"):
            with patch.object(cli, "parse_args", return_value=args), patch.object(
                cli,
                "get_client",
                return_value=client("group/Project", "group/project", "group/ok"),
            ), patch.object(
                cli, "filesystem_is_case_insensitive", return_value=True
            ), patch.object(
                cli,
                "backup_repository",
                side_effect=lambda a, i: attempted.append(i.path_with_namespace),
            ):
                with pytest.raises(Exception) as exc_info:
                    cli.main()

        assert attempted == ["group/ok"]
        assert "share one directory" in caplog.text
        assert "2 of 3 repositories failed" in str(exc_info.value)

    def test_namespaces_differing_in_case_also_collide(self, create_args, tmp_path):
        args = create_args(output_directory=str(tmp_path))

        with patch.object(cli, "parse_args", return_value=args), patch.object(
            cli, "get_client", return_value=client("Group/p", "group/p")
        ), patch.object(
            cli, "filesystem_is_case_insensitive", return_value=True
        ), patch.object(
            cli, "backup_repository"
        ) as mock_backup:
            with pytest.raises(Exception):
                cli.main()

        mock_backup.assert_not_called()

    def test_distinct_paths_are_unaffected(self, create_args, tmp_path):
        args = create_args(output_directory=str(tmp_path))

        with patch.object(cli, "parse_args", return_value=args), patch.object(
            cli, "get_client", return_value=client("group/a", "group/b")
        ), patch.object(
            cli, "filesystem_is_case_insensitive", return_value=True
        ), patch.object(
            cli, "backup_repository"
        ) as mock_backup:
            cli.main()

        assert mock_backup.call_count == 2

    def test_find_colliding_paths_groups_only_the_clashes(self):
        groups = cli.find_colliding_paths({"g/A": 1, "g/a": 2, "g/b": 3, "G/A": 4})

        assert groups == [["G/A", "g/A", "g/a"]]


class TestCaseSensitiveFilesystems:
    """On ext4 two paths differing only in case are distinct directories, so
    refusing to back both up there would be wrong."""

    def test_collisions_are_ignored_on_a_case_sensitive_filesystem(
        self, create_args, tmp_path
    ):
        args = create_args(output_directory=str(tmp_path))

        with patch.object(cli, "parse_args", return_value=args), patch.object(
            cli, "get_client", return_value=client("group/Project", "group/project")
        ), patch.object(
            cli, "filesystem_is_case_insensitive", return_value=False
        ), patch.object(
            cli, "backup_repository"
        ) as mock_backup:
            cli.main()

        assert mock_backup.call_count == 2

    def test_collisions_are_caught_on_a_case_insensitive_filesystem(
        self, create_args, tmp_path
    ):
        args = create_args(output_directory=str(tmp_path))

        with patch.object(cli, "parse_args", return_value=args), patch.object(
            cli, "get_client", return_value=client("group/Project", "group/project")
        ), patch.object(
            cli, "filesystem_is_case_insensitive", return_value=True
        ), patch.object(
            cli, "backup_repository"
        ) as mock_backup:
            with pytest.raises(Exception):
                cli.main()

        mock_backup.assert_not_called()

    def test_the_probe_agrees_with_the_real_filesystem(self, tmp_path):
        marker = tmp_path / "AAA"
        marker.write_text("")
        expected = (tmp_path / "aaa").exists()

        assert cli.filesystem_is_case_insensitive(str(tmp_path)) is expected

    def test_an_unwritable_directory_assumes_the_risky_case(self, tmp_path):
        assert cli.filesystem_is_case_insensitive(str(tmp_path / "missing")) is True

    def test_the_probe_leaves_nothing_behind(self, tmp_path):
        before = set(os.listdir(str(tmp_path)))

        cli.filesystem_is_case_insensitive(str(tmp_path))

        assert set(os.listdir(str(tmp_path))) == before


class TestCollisionsRespectTheNamespaceFilter:
    def test_collisions_outside_the_namespace_do_not_fail_the_run(
        self, create_args, tmp_path
    ):
        """A clash among projects this run is not backing up is not its problem."""
        args = create_args(output_directory=str(tmp_path), namespace="wanted")
        attempted = []

        with patch.object(cli, "parse_args", return_value=args), patch.object(
            cli,
            "get_client",
            return_value=client("other/Proj", "other/proj", "wanted/keep"),
        ), patch.object(
            cli, "filesystem_is_case_insensitive", return_value=True
        ), patch.object(
            cli,
            "backup_repository",
            side_effect=lambda a, i: attempted.append(i.path_with_namespace),
        ):
            cli.main()

        assert attempted == ["wanted/keep"]

    def test_collisions_inside_the_namespace_still_fail(self, create_args, tmp_path):
        args = create_args(output_directory=str(tmp_path), namespace="wanted")

        with patch.object(cli, "parse_args", return_value=args), patch.object(
            cli, "get_client", return_value=client("wanted/P", "wanted/p")
        ), patch.object(
            cli, "filesystem_is_case_insensitive", return_value=True
        ), patch.object(
            cli, "backup_repository"
        ):
            with pytest.raises(Exception) as exc_info:
                cli.main()

        assert "2 of 2 repositories failed" in str(exc_info.value)


class TestUnreadableProjects:
    """A project the filter cannot evaluate must cost only itself. It used to
    raise KeyError out of the loop and abort the whole run."""

    def test_one_malformed_project_does_not_abort_the_run(
        self, create_args, tmp_path, caplog
    ):
        args = create_args(output_directory=str(tmp_path), namespace="g")
        broken = type("P", (), {"path_with_namespace": "g/bad", "attributes": {}})()
        listing = type(
            "C",
            (),
            {
                "projects": type(
                    "L",
                    (),
                    {"list": lambda *a, **kw: [broken, project("g/good")]},
                )()
            },
        )()
        attempted = []

        with caplog.at_level(logging.ERROR, logger="gitlab_backup.gitlab_backup"):
            with patch.object(cli, "parse_args", return_value=args), patch.object(
                cli, "get_client", return_value=listing
            ), patch.object(
                cli,
                "backup_repository",
                side_effect=lambda a, i: attempted.append(i.path_with_namespace),
            ):
                with pytest.raises(Exception) as exc_info:
                    cli.main()

        assert attempted == ["g/good"]
        assert "Could not read project g/bad" in caplog.text
        assert "1 of 2 repositories failed" in str(exc_info.value)


class TestProjectsWithoutAPath:
    """repositories[None] used to crash find_colliding_paths with
    AttributeError: 'NoneType' object has no attribute 'casefold'."""

    @staticmethod
    def _listing(*projects):
        return type(
            "C",
            (),
            {"projects": type("L", (), {"list": lambda *a, **kw: list(projects)})()},
        )()

    @pytest.mark.parametrize("bad_path", [None, "", 42])
    def test_a_project_without_a_path_is_skipped(
        self, create_args, tmp_path, bad_path, caplog
    ):
        args = create_args(output_directory=str(tmp_path))
        broken = type(
            "P",
            (),
            {
                "path_with_namespace": bad_path,
                "attributes": {
                    "namespace": {"full_path": "g"},
                    "path_with_namespace": bad_path,
                },
            },
        )()
        attempted = []

        with caplog.at_level(logging.ERROR, logger="gitlab_backup.gitlab_backup"):
            with patch.object(cli, "parse_args", return_value=args), patch.object(
                cli, "get_client", return_value=self._listing(broken, project("g/ok"))
            ), patch.object(
                cli,
                "backup_repository",
                side_effect=lambda a, i: attempted.append(i.path_with_namespace),
            ):
                with pytest.raises(Exception) as exc_info:
                    cli.main()

        assert attempted == ["g/ok"]
        assert "no usable path" in caplog.text
        assert "1 of 2 repositories failed" in str(exc_info.value)

    def test_a_project_missing_the_attribute_entirely_is_skipped(
        self, create_args, tmp_path
    ):
        args = create_args(output_directory=str(tmp_path))
        broken = type("P", (), {"attributes": {}})()

        with patch.object(cli, "parse_args", return_value=args), patch.object(
            cli, "get_client", return_value=self._listing(broken)
        ), patch.object(cli, "backup_repository") as mock_backup:
            with pytest.raises(Exception):
                cli.main()

        mock_backup.assert_not_called()


class TestCaseProbeRobustness:
    def test_an_unremovable_probe_does_not_fail_the_run(self, tmp_path, monkeypatch):
        """A scanner holding the probe file must not abort the backup."""
        monkeypatch.setattr(cli.os, "unlink", _raise_permission_error)

        assert cli.filesystem_is_case_insensitive(str(tmp_path)) in (True, False)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
