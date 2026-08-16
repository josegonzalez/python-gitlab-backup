"""Tests for logging_subprocess pipe handling."""

import logging
import subprocess
import sys
import threading

import pytest

from gitlab_backup import gitlab_backup


def _raise_file_not_found(*_args, **_kwargs):
    raise FileNotFoundError(2, "No such file or directory", "git")


class TestLoggingSubprocess:
    """Test suite for logging_subprocess deadlock and logging behavior."""

    def test_large_stderr_output_does_not_deadlock(self):
        """Child output larger than the OS pipe buffer must not hang.

        The pipes are drained from threads; if they were not, the child would
        block once its output exceeded the pipe buffer (~8KB) and the parent
        would spin forever waiting on it.
        """
        # Write 256KB to stderr, far past any platform's pipe buffer
        child_code = (
            "import sys\n"
            "for _ in range(3200):\n"
            "    sys.stderr.write('x' * 79 + '\\n')\n"
        )
        result = {}

        def run():
            result["rc"] = gitlab_backup.logging_subprocess(
                [sys.executable, "-c", child_code]
            )

        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        thread.join(timeout=30)

        assert not thread.is_alive(), "logging_subprocess deadlocked on large output"
        assert result["rc"] == 0

    def test_stdout_logged_at_debug_stderr_at_error(self, caplog):
        """stdout lines log at DEBUG and stderr lines at ERROR."""
        child_code = (
            "import sys\n"
            "print('to stdout')\n"
            "print('to stderr', file=sys.stderr)\n"
        )

        with caplog.at_level(logging.DEBUG, logger="gitlab_backup.gitlab_backup"):
            rc = gitlab_backup.logging_subprocess([sys.executable, "-c", child_code])

        assert rc == 0
        records = [
            (r.levelno, r.getMessage())
            for r in caplog.records
            if r.name == "gitlab_backup.gitlab_backup"
        ]
        assert (logging.DEBUG, str(b"to stdout")) in records
        assert (logging.ERROR, str(b"to stderr")) in records

    def test_trailing_newlines_stripped(self, caplog):
        """Logged lines have trailing \\r\\n stripped, including Windows CRLF."""
        child_code = (
            "import sys\n"
            "sys.stdout.buffer.write(b'crlf line\\r\\n')\n"
            "sys.stdout.buffer.write(b'lf line\\n')\n"
        )

        with caplog.at_level(logging.DEBUG, logger="gitlab_backup.gitlab_backup"):
            rc = gitlab_backup.logging_subprocess([sys.executable, "-c", child_code])

        assert rc == 0
        messages = [
            r.getMessage()
            for r in caplog.records
            if r.name == "gitlab_backup.gitlab_backup"
        ]
        assert str(b"crlf line") in messages
        assert str(b"lf line") in messages

    def test_final_line_without_newline_not_truncated(self, caplog):
        """A final line with no trailing newline keeps its last character.

        The old code stripped the newline with line[:-1], which chopped the
        last character off any line that did not end with a newline.
        """
        child_code = "import sys\nsys.stdout.write('no newline')\n"

        with caplog.at_level(logging.DEBUG, logger="gitlab_backup.gitlab_backup"):
            rc = gitlab_backup.logging_subprocess([sys.executable, "-c", child_code])

        assert rc == 0
        messages = [
            r.getMessage()
            for r in caplog.records
            if r.name == "gitlab_backup.gitlab_backup"
        ]
        assert str(b"no newline") in messages

    def test_returns_child_exit_code(self, capsys):
        """Non-zero child exit codes are returned and summarized on stderr."""
        rc = gitlab_backup.logging_subprocess(
            [sys.executable, "-c", "import sys; sys.exit(3)"]
        )

        assert rc == 3
        captured = capsys.readouterr()
        assert "returned 3" in captured.err

    def test_cwd_is_forwarded_to_the_child(self, tmp_path, caplog):
        """Keyword arguments reach subprocess.Popen, so cwd works as expected."""
        child_code = "import os\nprint(os.getcwd())\n"

        with caplog.at_level(logging.DEBUG, logger="gitlab_backup.gitlab_backup"):
            rc = gitlab_backup.logging_subprocess(
                [sys.executable, "-c", child_code], cwd=str(tmp_path)
            )

        assert rc == 0
        messages = " ".join(
            r.getMessage()
            for r in caplog.records
            if r.name == "gitlab_backup.gitlab_backup"
        )
        assert tmp_path.name in messages


class TestCredentialMasking:
    """A failing git command must not print credentials to stderr."""

    def test_extra_header_is_redacted_in_failure_output(self, capsys):
        rc = gitlab_backup.logging_subprocess(
            [
                sys.executable,
                "-c",
                "import sys; sys.exit(1)",
                "http.extraHeader=Authorization: Basic b2F1dGgyOmdscGF0LXNlY3JldA==",
            ]
        )

        assert rc == 1
        captured = capsys.readouterr()
        assert "b2F1dGgyOmdscGF0LXNlY3JldA==" not in captured.err
        assert "http.extraHeader=*****" in captured.err

    def test_url_password_is_redacted_in_failure_output(self, capsys):
        rc = gitlab_backup.logging_subprocess(
            [
                sys.executable,
                "-c",
                "import sys; sys.exit(1)",
                "https://someone:hunter2@gitlab.example.com/group/project.git",
            ]
        )

        assert rc == 1
        captured = capsys.readouterr()
        assert "hunter2" not in captured.err
        assert "*****" in captured.err

    def test_ordinary_arguments_are_left_alone(self):
        assert gitlab_backup.mask_command(["git", "fetch", "--all"]) == [
            "git",
            "fetch",
            "--all",
        ]


class TestRunGit:
    def test_success_returns_zero(self):
        assert gitlab_backup.run_git([sys.executable, "-c", "pass"]) == 0

    def test_failure_raises_with_a_masked_command(self):
        with pytest.raises(gitlab_backup.GitCommandError) as exc_info:
            gitlab_backup.run_git(
                [
                    sys.executable,
                    "-c",
                    "import sys; sys.exit(7)",
                    "https://someone:hunter2@gitlab.example.com/x.git",
                ]
            )

        assert "exited with code 7" in str(exc_info.value)
        assert "hunter2" not in str(exc_info.value)


class TestRunGitRetries:
    """Retries must not repeat a command that is no longer safe to repeat."""

    @staticmethod
    def _failing(rc=1):
        return [sys.executable, "-c", "import sys; sys.exit({0})".format(rc)]

    def test_retries_until_the_limit(self, monkeypatch):
        monkeypatch.setattr(gitlab_backup.time, "sleep", lambda _s: None)
        calls = []
        real = gitlab_backup.logging_subprocess

        def counting(popenargs, **kwargs):
            calls.append(popenargs)
            return real(popenargs, **kwargs)

        monkeypatch.setattr(gitlab_backup, "logging_subprocess", counting)

        with pytest.raises(gitlab_backup.GitCommandError):
            gitlab_backup.run_git(self._failing(), retries=2)

        assert len(calls) == 3

    def test_retry_if_can_veto_a_retry(self, monkeypatch):
        """git removes a directory it created when a clone fails; if something
        still occupies the path, repeating the clone would fail differently."""
        monkeypatch.setattr(gitlab_backup.time, "sleep", lambda _s: None)
        calls = []
        real = gitlab_backup.logging_subprocess

        def counting(popenargs, **kwargs):
            calls.append(popenargs)
            return real(popenargs, **kwargs)

        monkeypatch.setattr(gitlab_backup, "logging_subprocess", counting)

        with pytest.raises(gitlab_backup.GitCommandError):
            gitlab_backup.run_git(self._failing(), retries=5, retry_if=lambda: False)

        assert len(calls) == 1

    def test_backoff_widens_between_attempts(self, monkeypatch):
        pauses = []
        monkeypatch.setattr(gitlab_backup.time, "sleep", pauses.append)

        with pytest.raises(gitlab_backup.GitCommandError):
            gitlab_backup.run_git(self._failing(), retries=3)

        assert pauses == sorted(pauses)
        assert len(pauses) == 3
        assert pauses[0] < pauses[-1]

    def test_a_successful_command_is_not_retried(self, monkeypatch):
        monkeypatch.setattr(gitlab_backup.time, "sleep", lambda _s: None)

        assert gitlab_backup.run_git([sys.executable, "-c", "pass"], retries=3) == 0


class TestTimeoutKillsTheChild:
    def test_a_hung_command_is_killed_and_reported(self, caplog):
        """Without this the process waits for ever on a dead connection."""
        with caplog.at_level(logging.ERROR, logger="gitlab_backup.gitlab_backup"):
            rc = gitlab_backup.logging_subprocess(
                [sys.executable, "-c", "import time; time.sleep(30)"], timeout=1
            )

        assert rc == gitlab_backup.TIMEOUT_RETURNCODE
        assert "exceeded the 1s timeout" in caplog.text

    def test_a_prompt_command_is_unaffected(self):
        assert (
            gitlab_backup.logging_subprocess([sys.executable, "-c", "pass"], timeout=30)
            == 0
        )


class TestProbeRemote:
    """The reachability probe retries like the fetch and clone that follow it,
    so a blip there does not fail an otherwise healthy repository."""

    UNREACHABLE = "/nonexistent/definitely-not-a-repo.git"

    def test_an_unreachable_remote_is_retried(self, monkeypatch):
        pauses = []
        monkeypatch.setattr(gitlab_backup.time, "sleep", pauses.append)

        rc = gitlab_backup.probe_remote(self.UNREACHABLE, retries=2)

        assert rc != 0
        assert len(pauses) == 2

    def test_no_retries_when_disabled(self, monkeypatch):
        pauses = []
        monkeypatch.setattr(gitlab_backup.time, "sleep", pauses.append)

        assert gitlab_backup.probe_remote(self.UNREACHABLE, retries=0) != 0
        assert pauses == []

    def test_a_reachable_remote_is_not_retried(self, tmp_path, monkeypatch):
        pauses = []
        monkeypatch.setattr(gitlab_backup.time, "sleep", pauses.append)
        repo = tmp_path / "origin.git"
        subprocess.run(["git", "init", "-q", "--bare", str(repo)], check=True)

        assert gitlab_backup.probe_remote(str(repo), retries=3) == 0
        assert pauses == []

    def test_a_hung_probe_is_killed(self, caplog):
        with caplog.at_level(logging.ERROR, logger="gitlab_backup.gitlab_backup"):
            rc = gitlab_backup.probe_remote("https://10.255.255.1/x.git", timeout=1)

        assert rc == gitlab_backup.TIMEOUT_RETURNCODE
        assert "exceeded the 1s timeout" in caplog.text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
