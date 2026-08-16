"""Tests for the CLI entry point wiring."""

import logging
import os
from unittest.mock import patch

import pytest

from gitlab_backup import cli


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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
