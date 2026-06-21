"""Email validation utilities for the Mailer application."""

import re
from typing import Optional


class EmailValidator:
    """Validates email addresses using RFC 5322 compliant pattern."""

    PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    @staticmethod
    def validate(email: str) -> bool:
        """Validate email address format.

        Args:
            email: Email address to validate

        Returns:
            True if email is valid, False otherwise

        Example:
            >>> EmailValidator.validate("user@example.com")
            True
            >>> EmailValidator.validate("invalid@")
            False
        """
        if not email or not isinstance(email, str):
            return False
        return bool(re.match(EmailValidator.PATTERN, email.strip()))

    @staticmethod
    def validate_or_raise(email: str) -> str:
        """Validate email and raise exception if invalid.

        Args:
            email: Email address to validate

        Returns:
            Stripped email address if valid

        Raises:
            ValueError: If email format is invalid
        """
        stripped = email.strip() if isinstance(email, str) else ""
        if not EmailValidator.validate(stripped):
            raise ValueError(f"Invalid email address: {email}")
        return stripped
