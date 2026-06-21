"""Tests for subscriber management module."""

import os
import pytest
import tempfile
from mailer.subscribers import SubscriberManager


@pytest.fixture
def temp_storage():
    """Create temporary storage file for testing.

    Yields:
        Path to temporary storage file
    """
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)


@pytest.fixture
def manager(temp_storage):
    """Create SubscriberManager instance for testing.

    Args:
        temp_storage: Temporary storage file path

    Yields:
        SubscriberManager instance
    """
    return SubscriberManager(storage_path=temp_storage)


class TestSubscriberManager:
    """Test cases for SubscriberManager class."""

    def test_add_subscriber_success(self, manager: SubscriberManager):
        """Test adding new subscriber."""
        result = manager.add_subscriber("user@example.com")
        assert result is True
        assert manager.count() == 1

    def test_add_subscriber_duplicate(self, manager: SubscriberManager):
        """Test adding duplicate subscriber returns False."""
        manager.add_subscriber("user@example.com")
        result = manager.add_subscriber("user@example.com")
        assert result is False
        assert manager.count() == 1

    def test_add_subscriber_case_insensitive(self, manager: SubscriberManager):
        """Test adding same email with different case."""
        manager.add_subscriber("User@Example.COM")
        result = manager.add_subscriber("user@example.com")
        assert result is False
        assert manager.count() == 1

    def test_add_subscriber_invalid_email(self, manager: SubscriberManager):
        """Test adding invalid email raises ValueError."""
        with pytest.raises(ValueError):
            manager.add_subscriber("invalid-email")

    def test_remove_subscriber_success(self, manager: SubscriberManager):
        """Test removing existing subscriber."""
        manager.add_subscriber("user@example.com")
        result = manager.remove_subscriber("user@example.com")
        assert result is True
        assert manager.count() == 0

    def test_remove_subscriber_not_found(self, manager: SubscriberManager):
        """Test removing non-existent subscriber returns False."""
        result = manager.remove_subscriber("nonexistent@example.com")
        assert result is False

    def test_get_subscribers(self, manager: SubscriberManager):
        """Test getting all subscribers."""
        emails = ["user1@example.com", "user2@example.com"]
        for email in emails:
            manager.add_subscriber(email)

        subscribers = manager.get_subscribers()
        assert len(subscribers) == 2
        assert sorted(subscribers) == sorted(emails)

    def test_get_subscribers_sorted(self, manager: SubscriberManager):
        """Test subscribers are returned sorted."""
        manager.add_subscriber("zebra@example.com")
        manager.add_subscriber("alpha@example.com")

        subscribers = manager.get_subscribers()
        assert subscribers == ["alpha@example.com", "zebra@example.com"]

    def test_count(self, manager: SubscriberManager):
        """Test counting subscribers."""
        assert manager.count() == 0

        manager.add_subscriber("user1@example.com")
        assert manager.count() == 1

        manager.add_subscriber("user2@example.com")
        assert manager.count() == 2

    def test_clear(self, manager: SubscriberManager):
        """Test clearing all subscribers."""
        manager.add_subscriber("user1@example.com")
        manager.add_subscriber("user2@example.com")
        assert manager.count() == 2

        manager.clear()
        assert manager.count() == 0

    def test_persistence(self, temp_storage: str):
        """Test subscribers persist across instances."""
        manager1 = SubscriberManager(storage_path=temp_storage)
        manager1.add_subscriber("user@example.com")
        assert manager1.count() == 1

        manager2 = SubscriberManager(storage_path=temp_storage)
        assert manager2.count() == 1
        assert "user@example.com" in manager2.get_subscribers()
