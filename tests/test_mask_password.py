"""Tests for mask_password."""

import pytest

from gitlab_backup.gitlab_backup import mask_command, mask_password


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


class TestMaskPasswordKeepsTheUrlReadable:
    """A blind substring replace used to redact the host and path too, so the
    log line no longer said which repository had failed."""

    def test_password_matching_the_host_only_masks_the_password(self):
        masked = mask_password("https://git:git@git.example.com/git/git.git")

        assert masked == "https://git:*****@git.example.com/git/git.git"

    def test_single_character_password_does_not_shred_the_url(self):
        masked = mask_password("https://u:a@gitlab.example.com/group/a-project.git")

        assert masked == "https://u:*****@gitlab.example.com/group/a-project.git"

    def test_port_is_preserved(self):
        masked = mask_password("https://u:pw@gitlab.example.com:8443/g/p.git")

        assert masked == "https://u:*****@gitlab.example.com:8443/g/p.git"

    def test_host_case_is_preserved(self):
        masked = mask_password("https://u:pw@GitLab.Example.COM/g/p.git")

        assert masked == "https://u:*****@GitLab.Example.COM/g/p.git"

    def test_query_and_fragment_survive(self):
        masked = mask_password("https://u:pw@host.example.com/p.git?a=1#frag")

        assert masked == "https://u:*****@host.example.com/p.git?a=1#frag"


class TestMaskCommandHeaderForms:
    """The header is redacted however it is spelled, not only when the argument
    starts with it."""

    TOKEN = "b2F1dGgyOnNlY3JldA=="

    def test_bare_config_argument(self):
        arg = "http.extraHeader=Authorization: Basic {0}".format(self.TOKEN)

        assert mask_command([arg]) == ["http.extraHeader=*****"]

    def test_argument_joined_with_dash_c(self):
        arg = "-c http.extraHeader=Authorization: Basic {0}".format(self.TOKEN)

        masked = mask_command([arg])[0]

        assert self.TOKEN not in masked
        assert masked == "-c http.extraHeader=*****"

    def test_argument_joined_with_config(self):
        arg = "--config=http.extraHeader=Authorization: Basic {0}".format(self.TOKEN)

        masked = mask_command([arg])[0]

        assert self.TOKEN not in masked

    def test_ordinary_arguments_survive(self):
        assert mask_command(["git", "fetch", "--all"]) == ["git", "fetch", "--all"]

    def test_non_string_arguments_are_tolerated(self):
        assert mask_command([1, None]) == ["1", "None"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
