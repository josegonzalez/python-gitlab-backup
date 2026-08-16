"""Tests for repository selection, URL choice, and git auth arguments."""

import base64
import logging

import pytest

from gitlab_backup.gitlab_backup import (
    get_git_extra_args,
    get_repo_url,
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


class TestGetGitExtraArgs:
    def test_no_token_yields_no_args(self, create_args):
        args = create_args()

        assert get_git_extra_args(args) == []

    def test_private_token_becomes_basic_auth_header(self, create_args):
        args = create_args(private_token="glpat-secret")

        extra_args = get_git_extra_args(args)

        expected = base64.b64encode(b"oauth2:glpat-secret").decode("utf-8")
        assert extra_args == [
            "-c",
            "http.extraHeader=Authorization: Basic {0}".format(expected),
        ]

    def test_oauth_token_becomes_basic_auth_header(self, create_args):
        args = create_args(oauth_token="oauth-secret")

        extra_args = get_git_extra_args(args)

        expected = base64.b64encode(b"oauth2:oauth-secret").decode("utf-8")
        assert extra_args == [
            "-c",
            "http.extraHeader=Authorization: Basic {0}".format(expected),
        ]

    def test_private_token_wins_over_oauth_token(self, create_args):
        args = create_args(private_token="glpat-secret", oauth_token="oauth-secret")

        header = get_git_extra_args(args)[1]

        assert base64.b64encode(b"oauth2:glpat-secret").decode("utf-8") in header


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
