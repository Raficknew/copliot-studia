"""Subscriber management module."""

import json
import os
from typing import List, Optional, Set
from pathlib import Path

from mailer.validators import EmailValidator


class SubscriberManager:
    """Manages mailing list subscribers."""

    def __init__(self, storage_path: str = "subscribers.json"):
        """Initialize subscriber manager.

        Args:
            storage_path: Path to JSON file for storing subscribers
        """
        self.storage_path = storage_path
        self._subscribers: Set[str] = set()
        self._load_subscribers()

    def _load_subscribers(self) -> None:
        """Load subscribers from storage file."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._subscribers = set(data.get("subscribers", []))
            except (json.JSONDecodeError, IOError):
                self._subscribers = set()

    def _save_subscribers(self) -> None:
        """Save subscribers to storage file."""
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump({"subscribers": list(self._subscribers)}, f, indent=2)
        except IOError as e:
            raise IOError(f"Failed to save subscribers: {e}") from e

    def add_subscriber(self, email: str) -> bool:
        """Add a new subscriber to the mailing list.

        Args:
            email: Email address to add

        Returns:
            True if added successfully, False if already exists

        Raises:
            ValueError: If email format is invalid
        """
        sanitized = EmailValidator.sanitize(email)
        if not sanitized:
            raise ValueError(f"Invalid email format: {email}")

        if sanitized in self._subscribers:
            return False

        self._subscribers.add(sanitized)
        self._save_subscribers()
        return True

    def remove_subscriber(self, email: str) -> bool:
        """Remove a subscriber from the mailing list.

        Args:
            email: Email address to remove

        Returns:
            True if removed successfully, False if not found
        """
        sanitized = EmailValidator.sanitize(email)
        if not sanitized or sanitized not in self._subscribers:
            return False

        self._subscribers.remove(sanitized)
        self._save_subscribers()
        return True

    def get_subscribers(self) -> List[str]:
        """Get all subscribers.

        Returns:
            List of subscriber email addresses
        """
        return sorted(list(self._subscribers))

    def count(self) -> int:
        """Get total number of subscribers.

        Returns:
            Number of subscribers
        """
        return len(self._subscribers)

    def clear(self) -> None:
        """Remove all subscribers."""
        self._subscribers.clear()
        self._save_subscribers()
