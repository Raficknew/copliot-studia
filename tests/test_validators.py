"""Tests for email validation functionality."""

import pytest
from mailer.validators import EmailValidator


class TestEmailValidator:
    """Test suite for EmailValidator class."""

    @pytest.mark.parametrize(
        "email,expected",
        [
            ("user@example.com", True),
            ("user+tag@domain.co.uk", True),
            ("test.user@subdomain.example.com", True),
            ("user_name@example.com", True),
            ("user-name@example.com", True),
            ("123@example.com", True),
            ("invalid@", False),
            ("@domain.com", False),
            ("user", False),
            ("user@", False),
            ("@", False),
            ("", False),
            ("user @example.com", False),
            ("user@domain", False),
            ("user@.com", False),
        ],
    )
    def test_validate_email_format(self, email: str, expected: bool) -> None:
        """Test email validation with various formats.

        Args:
            email: Email address to validate
            expected: Expected validation result
        """
        assert EmailValidator.validate(email) == expected

    def test_validate_with_none(self) -> None:
        """Test validation with None value returns False."""
        assert EmailValidator.validate(None) == False

    def test_validate_with_non_string(self) -> None:
        """Test validation with non-string value returns False."""
        assert EmailValidator.validate(123) == False
        assert EmailValidator.validate([]) == False
        assert EmailValidator.validate({}) == False

    def test_validate_or_raise_success(self) -> None:
        """Test validate_or_raise with valid email returns stripped email."""
        email = "  user@example.com  "
        result = EmailValidator.validate_or_raise(email)
        assert result == "user@example.com"

    def test_validate_or_raise_invalid_email(self) -> None:
        """Test validate_or_raise with invalid email raises ValueError."""
        with pytest.raises(ValueError, match="Invalid email address"):
            EmailValidator.validate_or_raise("invalid@")

    def test_validate_or_raise_empty_string(self) -> None:
        """Test validate_or_raise with empty string raises ValueError."""
        with pytest.raises(ValueError):
            EmailValidator.validate_or_raise("")

    def test_validate_strips_whitespace(self) -> None:
        """Test validation strips leading/trailing whitespace."""
        assert EmailValidator.validate("  user@example.com  ") == True
