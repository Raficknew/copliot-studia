"""Subscriber management for the Mailer application."""

from typing import List, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from .validators import EmailValidator


@dataclass
class Subscriber:
    """Represents a mailing list subscriber.

    Attributes:
        email: Subscriber's email address
        subscribed_at: Timestamp when subscription was created
        active: Whether the subscription is active
    """

    email: str
    subscribed_at: datetime = field(default_factory=datetime.now)
    active: bool = True

    def __post_init__(self) -> None:
        """Validate email after initialization."""
        self.email = EmailValidator.validate_or_raise(self.email)


class SubscriberManager:
    """Manages mailing list subscribers."""

    def __init__(self) -> None:
        """Initialize subscriber manager with empty list."""
        self._subscribers: Set[str] = set()

    def add_subscriber(self, email: str) -> bool:
        """Add a new subscriber to the mailing list.

        Args:
            email: Email address to add

        Returns:
            True if subscriber was added, False if already exists

        Raises:
            ValueError: If email format is invalid
        """
        validated_email = EmailValidator.validate_or_raise(email).lower()
        
        if validated_email in self._subscribers:
            return False
        
        self._subscribers.add(validated_email)
        return True

    def remove_subscriber(self, email: str) -> bool:
        """Remove a subscriber from the mailing list.

        Args:
            email: Email address to remove

        Returns:
            True if subscriber was removed, False if not found
        """
        email_lower = email.strip().lower()
        
        if email_lower in self._subscribers:
            self._subscribers.remove(email_lower)
            return True
        
        return False

    def get_subscribers(self) -> List[str]:
        """Get list of all subscribers.

        Returns:
            List of subscriber email addresses
        """
        return sorted(list(self._subscribers))

    def has_subscriber(self, email: str) -> bool:
        """Check if email is in subscriber list.

        Args:
            email: Email address to check

        Returns:
            True if subscriber exists, False otherwise
        """
        return email.strip().lower() in self._subscribers

    def get_subscriber_count(self) -> int:
        """Get total number of subscribers.

        Returns:
            Number of active subscribers
        """
        return len(self._subscribers)

    def clear_subscribers(self) -> None:
        """Remove all subscribers from the list."""
        self._subscribers.clear()
