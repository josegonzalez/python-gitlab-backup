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
    def test_username_and_password_authenticates(self, create_args):
        args = create_args(host=HOST, username="someone", password="hunter2")

        with patch("gitlab_backup.gitlab_backup.gitlab.Gitlab") as mock_gitlab:
            client = get_client(args)

        mock_gitlab.assert_called_once_with(
            HOST, email="someone", password="hunter2", ssl_verify=True
        )
        client.auth.assert_called_once_with()

    def test_missing_password_is_prompted_for(self, create_args):
        args = create_args(host=HOST, username="someone", password=None)

        with patch("gitlab_backup.gitlab_backup.gitlab.Gitlab") as mock_gitlab, patch(
            "gitlab_backup.gitlab_backup.getpass.getpass", return_value="prompted"
        ) as mock_getpass:
            get_client(args)

        mock_getpass.assert_called_once_with()
        mock_gitlab.assert_called_once_with(
            HOST, email="someone", password="prompted", ssl_verify=True
        )

    def test_empty_prompted_password_raises(self, create_args):
        args = create_args(host=HOST, username="someone", password=None)

        with patch("gitlab_backup.gitlab_backup.getpass.getpass", return_value=""):
            with pytest.raises(Exception) as exc_info:
                get_client(args)

        assert "You must specify a password for basic auth" in str(exc_info.value)


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
