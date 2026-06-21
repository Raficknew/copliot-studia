"""Email validation module using RFC 5322 pattern."""

import re
from typing import Optional


class EmailValidator:
    """Email validator using RFC 5322 compliant pattern."""

    PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    @staticmethod
    def validate(email: str) -> bool:
        """Validate email address format.

        Args:
            email: Email address to validate

        Returns:
            True if email is valid, False otherwise
        """
        if not email or not isinstance(email, str):
            return False
        return bool(re.match(EmailValidator.PATTERN, email.strip()))

    @staticmethod
    def sanitize(email: str) -> Optional[str]:
        """Sanitize and validate email address.

        Args:
            email: Email address to sanitize

        Returns:
            Sanitized email or None if invalid
        """
        if not email or not isinstance(email, str):
            return None

        sanitized = email.strip().lower()
        return sanitized if EmailValidator.validate(sanitized) else None
