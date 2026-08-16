"""Tests for gitlab client construction and authentication."""

import logging
from unittest.mock import patch

import pytest

from gitlab_backup.gitlab_backup import get_client

HOST = "https://gitlab.example.com"


class TestGetClientTokens:
    def test_private_token_is_passed_through(self, create_args):
        args = create_args(host=HOST, private_token="glpat-secret")

        with patch("gitlab_backup.gitlab_backup.gitlab.Gitlab") as mock_gitlab:
            client = get_client(args)

        mock_gitlab.assert_called_once_with(
            HOST, private_token="glpat-secret", ssl_verify=True
        )
        assert client is mock_gitlab.return_value

    def test_oauth_token_is_passed_through(self, create_args):
        args = create_args(host=HOST, oauth_token="oauth-secret")

        with patch("gitlab_backup.gitlab_backup.gitlab.Gitlab") as mock_gitlab:
            get_client(args)

        mock_gitlab.assert_called_once_with(
            HOST, oauth_token="oauth-secret", ssl_verify=True
        )

    def test_private_token_wins_over_oauth_token(self, create_args):
        args = create_args(
            host=HOST, private_token="glpat-secret", oauth_token="oauth-secret"
        )

        with patch("gitlab_backup.gitlab_backup.gitlab.Gitlab") as mock_gitlab:
            get_client(args)

        _, kwargs = mock_gitlab.call_args
        assert kwargs == {"private_token": "glpat-secret", "ssl_verify": True}

    def test_private_token_read_from_file_uri(self, create_args, tmp_path):
        token_file = tmp_path / "token"
        token_file.write_text("glpat-from-file\n")
        args = create_args(host=HOST, private_token="file://{0}".format(token_file))

        with patch("gitlab_backup.gitlab_backup.gitlab.Gitlab") as mock_gitlab:
            get_client(args)

        mock_gitlab.assert_called_once_with(
            HOST, private_token="glpat-from-file", ssl_verify=True
        )
        assert args.private_token == "glpat-from-file"

    def test_oauth_token_read_from_file_uri(self, create_args, tmp_path):
        token_file = tmp_path / "token"
        token_file.write_text("oauth-from-file\n")
        args = create_args(host=HOST, oauth_token="file://{0}".format(token_file))

        with patch("gitlab_backup.gitlab_backup.gitlab.Gitlab") as mock_gitlab:
            get_client(args)

        mock_gitlab.assert_called_once_with(
            HOST, oauth_token="oauth-from-file", ssl_verify=True
        )


class TestGetClientBasicAuth:
    """GitLab removed password authentication from its API and python-gitlab
    dropped the email=/password= arguments in 3.0, so these flags cannot work.
    They fail with a pointer to --private-token rather than a TypeError from
    deep inside the client library."""

    def test_username_raises_an_actionable_error(self, create_args):
        args = create_args(host=HOST, username="someone", password="hunter2")

        with pytest.raises(Exception) as exc_info:
            get_client(args)

        message = str(exc_info.value)
        assert "no longer usable" in message
        assert "--private-token" in message

    def test_username_without_password_also_raises(self, create_args):
        args = create_args(host=HOST, username="someone", password=None)

        with pytest.raises(Exception) as exc_info:
            get_client(args)

        assert "--private-token" in str(exc_info.value)

    def test_a_token_takes_precedence_over_username(self, create_args):
        """A config carrying both keeps working through the token path."""
        args = create_args(host=HOST, username="someone", private_token="glpat-secret")

        with patch("gitlab_backup.gitlab_backup.gitlab.Gitlab") as mock_gitlab:
            get_client(args)

        mock_gitlab.assert_called_once_with(
            HOST, private_token="glpat-secret", ssl_verify=True
        )


class TestRealClientSignature:
    """The other tests mock gitlab.Gitlab, so a mock would happily accept any
    keyword. This one constructs the real client to catch signature drift in
    python-gitlab, which is how the email=/password= breakage went unnoticed."""

    def test_supported_arguments_still_exist(self):
        import gitlab

        client = gitlab.Gitlab(HOST, private_token="glpat-secret", ssl_verify=True)
        assert client is not None

    def test_oauth_token_argument_still_exists(self):
        import gitlab

        client = gitlab.Gitlab(HOST, oauth_token="oauth-secret", ssl_verify=True)
        assert client is not None


class TestGetClientMisc:
    def test_anonymous_client_without_credentials(self, create_args):
        args = create_args(host=HOST)

        with patch("gitlab_backup.gitlab_backup.gitlab.Gitlab") as mock_gitlab:
            get_client(args)

        mock_gitlab.assert_called_once_with(HOST, ssl_verify=True)

    def test_disable_ssl_verification_inverts_ssl_verify(self, create_args):
        args = create_args(
            host=HOST, private_token="glpat-secret", disable_ssl_verification=True
        )

        with patch("gitlab_backup.gitlab_backup.gitlab.Gitlab") as mock_gitlab:
            get_client(args)

        _, kwargs = mock_gitlab.call_args
        assert kwargs["ssl_verify"] is False

    def test_missing_host_returns_none_and_logs(self, create_args, caplog):
        args = create_args(host=None, private_token="glpat-secret")

        with caplog.at_level(logging.ERROR, logger="gitlab_backup.gitlab_backup"):
            with patch("gitlab_backup.gitlab_backup.gitlab.Gitlab") as mock_gitlab:
                client = get_client(args)

        assert client is None
        mock_gitlab.assert_not_called()
        assert "Missing --host flag" in caplog.text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
