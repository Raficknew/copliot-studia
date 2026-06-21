"""Tests for subscriber management functionality."""

import pytest
from mailer.subscribers import SubscriberManager, Subscriber


class TestSubscriber:
    """Test suite for Subscriber class."""

    def test_create_subscriber_success(self) -> None:
        """Test creating subscriber with valid email."""
        subscriber = Subscriber(email="user@example.com")
        assert subscriber.email == "user@example.com"
        assert subscriber.active is True

    def test_create_subscriber_invalid_email(self) -> None:
        """Test creating subscriber with invalid email raises ValueError."""
        with pytest.raises(ValueError):
            Subscriber(email="invalid@")

    def test_subscriber_has_timestamp(self) -> None:
        """Test subscriber has subscribed_at timestamp."""
        subscriber = Subscriber(email="user@example.com")
        assert subscriber.subscribed_at is not None


class TestSubscriberManager:
    """Test suite for SubscriberManager class."""

    @pytest.fixture
    def manager(self) -> SubscriberManager:
        """Create SubscriberManager instance for testing."""
        return SubscriberManager()

    def test_add_subscriber_success(self, manager: SubscriberManager) -> None:
        """Test adding new subscriber returns True."""
        result = manager.add_subscriber("user@example.com")
        assert result is True
        assert manager.get_subscriber_count() == 1

    def test_add_duplicate_subscriber(self, manager: SubscriberManager) -> None:
        """Test adding duplicate subscriber returns False."""
        manager.add_subscriber("user@example.com")
        result = manager.add_subscriber("user@example.com")
        assert result is False
        assert manager.get_subscriber_count() == 1

    def test_add_subscriber_invalid_email(self, manager: SubscriberManager) -> None:
        """Test adding subscriber with invalid email raises ValueError."""
        with pytest.raises(ValueError):
            manager.add_subscriber("invalid@")

    def test_remove_subscriber_success(self, manager: SubscriberManager) -> None:
        """Test removing existing subscriber returns True."""
        manager.add_subscriber("user@example.com")
        result = manager.remove_subscriber("user@example.com")
        assert result is True
        assert manager.get_subscriber_count() == 0

    def test_remove_nonexistent_subscriber(self, manager: SubscriberManager) -> None:
        """Test removing non-existent subscriber returns False."""
        result = manager.remove_subscriber("user@example.com")
        assert result is False

    def test_get_subscribers_empty(self, manager: SubscriberManager) -> None:
        """Test getting subscribers from empty list returns empty list."""
        assert manager.get_subscribers() == []

    def test_get_subscribers_returns_sorted(self, manager: SubscriberManager) -> None:
        """Test get_subscribers returns sorted list."""
        manager.add_subscriber("zebra@example.com")
        manager.add_subscriber("alpha@example.com")
        manager.add_subscriber("beta@example.com")
        
        subscribers = manager.get_subscribers()
        assert subscribers == ["alpha@example.com", "beta@example.com", "zebra@example.com"]

    def test_has_subscriber_true(self, manager: SubscriberManager) -> None:
        """Test has_subscriber returns True for existing subscriber."""
        manager.add_subscriber("user@example.com")
        assert manager.has_subscriber("user@example.com") is True

    def test_has_subscriber_false(self, manager: SubscriberManager) -> None:
        """Test has_subscriber returns False for non-existent subscriber."""
        assert manager.has_subscriber("user@example.com") is False

    def test_get_subscriber_count(self, manager: SubscriberManager) -> None:
        """Test get_subscriber_count returns correct count."""
        assert manager.get_subscriber_count() == 0
        
        manager.add_subscriber("user1@example.com")
        assert manager.get_subscriber_count() == 1
        
        manager.add_subscriber("user2@example.com")
        assert manager.get_subscriber_count() == 2

    def test_clear_subscribers(self, manager: SubscriberManager) -> None:
        """Test clear_subscribers removes all subscribers."""
        manager.add_subscriber("user1@example.com")
        manager.add_subscriber("user2@example.com")
        
        manager.clear_subscribers()
        assert manager.get_subscriber_count() == 0
        assert manager.get_subscribers() == []

    def test_case_insensitive_email(self, manager: SubscriberManager) -> None:
        """Test email handling is case insensitive."""
        manager.add_subscriber("User@Example.COM")
        assert manager.has_subscriber("user@example.com") is True
