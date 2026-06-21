"""Tests for email validation module."""

import pytest
from mailer.validators import EmailValidator


class TestEmailValidator:
    """Test cases for EmailValidator class."""

    @pytest.mark.parametrize(
        "email,expected",
        [
            ("user@example.com", True),
            ("test.user@domain.co.uk", True),
            ("user+tag@example.com", True),
            ("user_name@example-domain.com", True),
            ("123@numbers.com", True),
            ("invalid@", False),
            ("@domain.com", False),
            ("user@", False),
            ("user", False),
            ("", False),
            ("user @example.com", False),
            ("user@domain", False),
            ("user@@domain.com", False),
            (None, False),
        ],
    )
    def test_validate(self, email: str, expected: bool) -> None:
        """Test email validation with various inputs.

        Args:
            email: Email to validate
            expected: Expected validation result
        """
        assert EmailValidator.validate(email) == expected

    def test_validate_with_whitespace(self) -> None:
        """Test validation strips whitespace."""
        assert EmailValidator.validate("  user@example.com  ") is True

    @pytest.mark.parametrize(
        "email,expected",
        [
            ("User@Example.COM", "user@example.com"),
            ("  TEST@DOMAIN.com  ", "test@domain.com"),
            ("invalid", None),
            ("", None),
            (None, None),
        ],
    )
    def test_sanitize(self, email: str, expected: str) -> None:
        """Test email sanitization.

        Args:
            email: Email to sanitize
            expected: Expected sanitized result
        """
        assert EmailValidator.sanitize(email) == expected
