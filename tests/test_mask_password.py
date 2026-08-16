"""Tests for mask_password."""

import pytest

from gitlab_backup.gitlab_backup import mask_password


class TestMaskPassword:
    """Credentials must never reach the logs verbatim."""

    def test_url_without_credentials_is_unchanged(self):
        url = "https://gitlab.example.com/group/project.git"

        assert mask_password(url) == url

    def test_url_with_username_only_is_unchanged(self):
        url = "https://someone@gitlab.example.com/group/project.git"

        assert mask_password(url) == url

    def test_password_is_masked(self):
        url = "https://someone:hunter2@gitlab.example.com/group/project.git"

        masked = mask_password(url)

        assert "hunter2" not in masked
        assert masked == "https://someone:*****@gitlab.example.com/group/project.git"

    def test_oauth_basic_masks_the_username_token(self):
        """With x-oauth-basic the token is the username, so mask that instead."""
        url = "https://glpat-secret:x-oauth-basic@gitlab.example.com/group/project.git"

        masked = mask_password(url)

        assert "glpat-secret" not in masked
        assert (
            masked == "https://*****:x-oauth-basic@gitlab.example.com/group/project.git"
        )

    def test_custom_secret_is_used(self):
        url = "https://someone:hunter2@gitlab.example.com/group/project.git"

        assert (
            mask_password(url, secret="[redacted]")
            == "https://someone:[redacted]@gitlab.example.com/group/project.git"
        )

    def test_ssh_url_is_unchanged(self):
        url = "git@gitlab.example.com:group/project.git"

        assert mask_password(url) == url


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
