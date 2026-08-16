"""Tests for CLI argument parsing."""

import pytest

from gitlab_backup.gitlab_backup import parse_args


class TestParseArgsDefaults:
    """Every flag has a defined default so callers never hit AttributeError."""

    def test_no_arguments_is_valid(self):
        """The parser has no required positional arguments."""
        args = parse_args([])

        assert args.host is None
        assert args.username is None
        assert args.password is None

    def test_token_defaults(self):
        args = parse_args([])

        assert args.oauth_token is None
        assert args.private_token is None

    def test_boolean_flags_default_to_false(self):
        args = parse_args([])

        assert args.clone_bare is False
        assert args.clone_lfs is False
        assert args.disable_ssl_verification is False
        assert args.prefer_ssh is False
        assert args.skip_existing is False
        assert args.owned_only is False
        assert args.with_membership is False
        assert args.quiet is False

    def test_value_defaults(self):
        args = parse_args([])

        assert args.namespace is None
        assert args.output_directory == "."
        assert args.private_key == ""
        assert args.log_level is None


class TestParseArgsFlags:
    """Flags map to the expected destinations."""

    @pytest.mark.parametrize(
        "flag,dest",
        [
            ("--clone-bare", "clone_bare"),
            ("--clone-lfs", "clone_lfs"),
            ("--disable-ssl-verification", "disable_ssl_verification"),
            ("--prefer-ssh", "prefer_ssh"),
            ("--skip-existing", "skip_existing"),
            ("--owned-only", "owned_only"),
            ("--with-membership", "with_membership"),
            ("--quiet", "quiet"),
        ],
    )
    def test_store_true_flags(self, flag, dest):
        assert getattr(parse_args([flag]), dest) is True

    @pytest.mark.parametrize(
        "flag,dest,value",
        [
            ("--host", "host", "https://gitlab.example.com"),
            ("--username", "username", "someone"),
            ("--password", "password", "hunter2"),
            ("--oauth-token", "oauth_token", "oauth-abc"),
            ("--private-token", "private_token", "glpat-abc"),
            ("--namespace", "namespace", "group/subgroup"),
            ("--output-directory", "output_directory", "/tmp/backup"),
            ("--private_key", "private_key", "/home/user/.ssh/id_ed25519"),
            ("--log-level", "log_level", "DEBUG"),
        ],
    )
    def test_value_flags(self, flag, dest, value):
        assert getattr(parse_args([flag, value]), dest) == value

    def test_unknown_flag_exits(self):
        with pytest.raises(SystemExit):
            parse_args(["--not-a-real-flag"])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
