"""Tests for repository selection, URL choice, and git auth arguments."""

import base64
import logging

import pytest

from gitlab_backup.gitlab_backup import (
    get_git_env,
    get_repo_url,
    read_token,
    should_include_repository,
)


def attributes(full_path="group", path_with_namespace="group/project"):
    return {
        "namespace": {"full_path": full_path},
        "path_with_namespace": path_with_namespace,
        "http_url_to_repo": "https://gitlab.example.com/group/project.git",
        "ssh_url_to_repo": "git@gitlab.example.com:group/project.git",
    }


class TestShouldIncludeRepository:
    def test_included_when_no_namespace_filter(self, create_args):
        args = create_args(namespace=None)

        assert should_include_repository(args, attributes()) is True

    def test_included_when_namespace_matches(self, create_args):
        args = create_args(namespace="group")

        assert should_include_repository(args, attributes(full_path="group")) is True

    def test_excluded_when_namespace_differs(self, create_args):
        args = create_args(namespace="other")

        assert should_include_repository(args, attributes(full_path="group")) is False

    def test_subgroup_namespace_matches_full_path(self, create_args):
        """The filter compares the full path, so a parent group does not match."""
        args = create_args(namespace="group")

        assert (
            should_include_repository(args, attributes(full_path="group/subgroup"))
            is False
        )

    def test_exclusion_is_logged_at_debug(self, create_args, caplog):
        args = create_args(namespace="other")

        with caplog.at_level(logging.DEBUG, logger="gitlab_backup.gitlab_backup"):
            should_include_repository(args, attributes())

        assert "Skipping group/project as namespace does not match other" in caplog.text


class TestGetRepoUrl:
    def test_https_by_default(self, create_args):
        args = create_args(prefer_ssh=False)

        assert get_repo_url(args, attributes()) == (
            "https://gitlab.example.com/group/project.git"
        )

    def test_ssh_when_preferred(self, create_args):
        args = create_args(prefer_ssh=True)

        assert get_repo_url(args, attributes()) == (
            "git@gitlab.example.com:group/project.git"
        )

    def test_missing_http_url_returns_none(self, create_args):
        args = create_args(prefer_ssh=False)
        attrs = attributes()
        del attrs["http_url_to_repo"]

        assert get_repo_url(args, attrs) is None

    def test_missing_ssh_url_returns_none(self, create_args):
        args = create_args(prefer_ssh=True)
        attrs = attributes()
        del attrs["ssh_url_to_repo"]

        assert get_repo_url(args, attrs) is None


class TestGetGitEnv:
    """The credential goes in the environment so it stays out of `ps`."""

    def test_no_token_leaves_git_config_untouched(self, create_args):
        args = create_args()

        env = get_git_env(args)

        assert "GIT_CONFIG_COUNT" not in env
        assert "GIT_CONFIG_KEY_0" not in env

    def test_private_token_becomes_a_git_config_entry(self, create_args):
        args = create_args(private_token="glpat-secret")

        env = get_git_env(args)

        expected = base64.b64encode(b"oauth2:glpat-secret").decode("utf-8")
        assert env["GIT_CONFIG_COUNT"] == "1"
        assert env["GIT_CONFIG_KEY_0"] == "http.extraHeader"
        assert env["GIT_CONFIG_VALUE_0"] == "Authorization: Basic {0}".format(expected)

    def test_oauth_token_becomes_a_git_config_entry(self, create_args):
        args = create_args(oauth_token="oauth-secret")

        env = get_git_env(args)

        expected = base64.b64encode(b"oauth2:oauth-secret").decode("utf-8")
        assert env["GIT_CONFIG_VALUE_0"] == "Authorization: Basic {0}".format(expected)

    def test_private_token_wins_over_oauth_token(self, create_args):
        args = create_args(private_token="glpat-secret", oauth_token="oauth-secret")

        env = get_git_env(args)

        expected = base64.b64encode(b"oauth2:glpat-secret").decode("utf-8")
        assert env["GIT_CONFIG_VALUE_0"] == "Authorization: Basic {0}".format(expected)

    def test_inherits_the_parent_environment(self, create_args, monkeypatch):
        monkeypatch.setenv("GIT_SSH_COMMAND", "ssh -i /key")
        args = create_args()

        assert get_git_env(args)["GIT_SSH_COMMAND"] == "ssh -i /key"

    def test_existing_git_config_entries_are_not_overwritten(
        self, create_args, monkeypatch
    ):
        """Appending at the next index keeps a caller's own GIT_CONFIG_* intact."""
        monkeypatch.setenv("GIT_CONFIG_COUNT", "1")
        monkeypatch.setenv("GIT_CONFIG_KEY_0", "user.name")
        monkeypatch.setenv("GIT_CONFIG_VALUE_0", "someone")
        args = create_args(private_token="glpat-secret")

        env = get_git_env(args)

        assert env["GIT_CONFIG_COUNT"] == "2"
        assert env["GIT_CONFIG_KEY_0"] == "user.name"
        assert env["GIT_CONFIG_KEY_1"] == "http.extraHeader"

    def test_unparseable_git_config_count_is_ignored(self, create_args, monkeypatch):
        monkeypatch.setenv("GIT_CONFIG_COUNT", "not-a-number")
        args = create_args(private_token="glpat-secret")

        env = get_git_env(args)

        assert env["GIT_CONFIG_COUNT"] == "1"
        assert env["GIT_CONFIG_KEY_0"] == "http.extraHeader"

    def test_token_never_appears_in_a_command_line(self, create_args):
        """Regression guard: the old implementation returned -c arguments."""
        args = create_args(private_token="glpat-secret")

        env = get_git_env(args)

        assert not any("glpat-secret" in key for key in env)


class TestReadToken:
    """get_git_env resolves file:// itself rather than relying on get_client
    having already rewritten args as a side effect."""

    def test_inline_token_is_returned_as_is(self):
        assert read_token("glpat-secret") == "glpat-secret"

    def test_none_is_passed_through(self):
        assert read_token(None) is None

    def test_file_uri_is_read_and_stripped(self, tmp_path):
        token_file = tmp_path / "token"
        token_file.write_text("glpat-from-file\n")

        assert read_token("file://{0}".format(token_file)) == "glpat-from-file"

    def test_git_env_resolves_a_file_uri_without_get_client(
        self, create_args, tmp_path
    ):
        token_file = tmp_path / "token"
        token_file.write_text("glpat-from-file\n")
        args = create_args(private_token="file://{0}".format(token_file))

        env = get_git_env(args)

        expected = base64.b64encode(b"oauth2:glpat-from-file").decode("utf-8")
        assert env["GIT_CONFIG_VALUE_0"] == "Authorization: Basic {0}".format(expected)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
