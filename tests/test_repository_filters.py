"""Tests for repository selection, URL choice, and git auth arguments."""

import base64
import logging

import pytest

from gitlab_backup.gitlab_backup import (
    get_git_env,
    get_repo_url,
    read_token,
    remote_host,
    remote_repo_path,
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

    def test_subgroups_are_included(self, create_args):
        """A namespace covers everything nested beneath it."""
        args = create_args(namespace="group")

        assert (
            should_include_repository(args, attributes(full_path="group/subgroup"))
            is True
        )

    def test_deeply_nested_subgroups_are_included(self, create_args):
        args = create_args(namespace="group")

        assert (
            should_include_repository(args, attributes(full_path="group/a/b/c")) is True
        )

    def test_namespace_matches_on_a_path_boundary(self, create_args):
        """--namespace group must not sweep in a sibling called groupother."""
        args = create_args(namespace="group")

        assert (
            should_include_repository(args, attributes(full_path="groupother")) is False
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
        args = create_args(stall_timeout=0)

        env = get_git_env(args)

        assert "GIT_CONFIG_COUNT" not in env
        assert "GIT_CONFIG_KEY_0" not in env

    def test_private_token_becomes_a_git_config_entry(self, create_args):
        args = create_args(private_token="glpat-secret", stall_timeout=0)

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
        args = create_args(private_token="glpat-secret", stall_timeout=0)

        env = get_git_env(args)

        assert env["GIT_CONFIG_COUNT"] == "2"
        assert env["GIT_CONFIG_KEY_0"] == "user.name"
        assert env["GIT_CONFIG_KEY_1"] == "http.extraHeader"

    def test_unparseable_git_config_count_is_ignored(self, create_args, monkeypatch):
        monkeypatch.setenv("GIT_CONFIG_COUNT", "not-a-number")
        args = create_args(private_token="glpat-secret", stall_timeout=0)

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


class TestStallDetection:
    """A dead connection used to hang the run for ever. git's own low-speed
    limit aborts a transfer that stops making progress, while leaving a merely
    slow but healthy download alone."""

    def test_stall_timeout_is_configured_by_default(self, create_args):
        args = create_args()

        env = get_git_env(args)
        config = dict(
            (env["GIT_CONFIG_KEY_{0}".format(i)], env["GIT_CONFIG_VALUE_{0}".format(i)])
            for i in range(int(env["GIT_CONFIG_COUNT"]))
        )

        assert config["http.lowSpeedTime"] == "60"
        assert int(config["http.lowSpeedLimit"]) > 0

    def test_stall_timeout_is_configurable(self, create_args):
        args = create_args(stall_timeout=15)

        env = get_git_env(args)
        config = dict(
            (env["GIT_CONFIG_KEY_{0}".format(i)], env["GIT_CONFIG_VALUE_{0}".format(i)])
            for i in range(int(env["GIT_CONFIG_COUNT"]))
        )

        assert config["http.lowSpeedTime"] == "15"

    def test_zero_disables_it(self, create_args):
        args = create_args(stall_timeout=0, private_token="glpat-secret")

        env = get_git_env(args)

        assert env["GIT_CONFIG_COUNT"] == "1"
        assert env["GIT_CONFIG_KEY_0"] == "http.extraHeader"

    def test_credential_and_stall_settings_coexist(self, create_args):
        args = create_args(private_token="glpat-secret", stall_timeout=30)

        env = get_git_env(args)
        keys = [
            env["GIT_CONFIG_KEY_{0}".format(i)]
            for i in range(int(env["GIT_CONFIG_COUNT"]))
        ]

        assert keys == ["http.extraHeader", "http.lowSpeedLimit", "http.lowSpeedTime"]


class TestRemoteIdentity:
    """A remote URL is reduced to host plus project path so the same project
    is recognised across transports, and a different one never is."""

    @pytest.mark.parametrize(
        "url,host,path",
        [
            ("https://gitlab.com/g/p.git", "gitlab.com", "g/p"),
            ("git@gitlab.com:g/p.git", "gitlab.com", "g/p"),
            ("ssh://git@GitLab.COM:22/g/p.git", "gitlab.com", "g/p"),
            ("https://user:pw@self.hosted:8443/g/p.git", "self.hosted", "g/p"),
            ("https://gitlab.com/g/sub/p", "gitlab.com", "g/sub/p"),
        ],
    )
    def test_urls_reduce_to_host_and_path(self, url, host, path):
        assert remote_host(url) == host
        assert remote_repo_path(url) == path

    def test_a_local_path_has_no_host(self):
        assert remote_host("/srv/mirrors/p.git") == ""
        assert remote_repo_path("/srv/mirrors/p.git") == "srv/mirrors/p"

    def test_empty_input(self):
        assert remote_host("") == ""
        assert remote_repo_path("") == ""

    def test_case_differences_in_the_path_are_preserved(self):
        """Path case must survive: it is what distinguishes the two projects."""
        assert remote_repo_path("https://h/G/P.git") != remote_repo_path(
            "https://h/g/p.git"
        )


class TestRemoteHostLocalPaths:
    """A local path is not a host. git applies the same drive-letter rule."""

    @pytest.mark.parametrize(
        "path",
        [
            "C:\\backups\\repo.git",
            "D:/backups/repo.git",
            "/srv/mirrors/repo.git",
            "./relative/repo.git",
            "../up/repo.git",
        ],
    )
    def test_local_paths_have_no_host(self, path):
        assert remote_host(path) == ""

    def test_a_real_host_is_still_recognised(self):
        assert remote_host("gitlab.example.com:group/project.git") == (
            "gitlab.example.com"
        )

    def test_a_single_letter_host_over_ssh_is_still_a_host(self):
        """Only the bare scp-like form is ambiguous; a scheme removes the doubt."""
        assert remote_host("ssh://git@c/group/project.git") == "c"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
