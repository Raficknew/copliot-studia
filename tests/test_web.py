"""Tests for Flask web application."""

import pytest
import json
from unittest.mock import patch, MagicMock
from mailer.web import app


@pytest.fixture
def client():
    """Create Flask test client.

    Yields:
        Flask test client
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_subscriber_manager():
    """Mock SubscriberManager for testing.

    Yields:
        Mocked SubscriberManager
    """
    with patch("mailer.web.subscriber_manager") as mock:
        yield mock


@pytest.fixture
def mock_email_sender():
    """Mock EmailSender for testing.

    Yields:
        Mocked EmailSender
    """
    with patch("mailer.web.email_sender") as mock:
        yield mock


class TestWebRoutes:
    """Test cases for Flask web routes."""

    def test_index_route(self, client):
        """Test main page renders successfully."""
        response = client.get("/")
        assert response.status_code == 200

    def test_subscribe_success(self, client, mock_subscriber_manager):
        """Test successful subscription."""
        mock_subscriber_manager.add_subscriber.return_value = True
        mock_subscriber_manager.count.return_value = 1

        response = client.post(
            "/api/subscribe",
            data=json.dumps({"email": "test@example.com"}),
            content_type="application/json",
        )

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["success"] is True
        assert data["count"] == 1

    def test_subscribe_invalid_email(self, client, mock_subscriber_manager):
        """Test subscription with invalid email format."""
        response = client.post(
            "/api/subscribe",
            data=json.dumps({"email": "invalid-email"}),
            content_type="application/json",
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["success"] is False
        assert "Invalid email" in data["error"]

    def test_subscribe_missing_email(self, client):
        """Test subscription without email field."""
        response = client.post(
            "/api/subscribe",
            data=json.dumps({}),
            content_type="application/json",
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["success"] is False

    def test_subscribe_duplicate(self, client, mock_subscriber_manager):
        """Test subscription with duplicate email."""
        mock_subscriber_manager.add_subscriber.return_value = False

        response = client.post(
            "/api/subscribe",
            data=json.dumps({"email": "test@example.com"}),
            content_type="application/json",
        )

        assert response.status_code == 409
        data = json.loads(response.data)
        assert data["success"] is False

    def test_unsubscribe_success(self, client, mock_subscriber_manager):
        """Test successful unsubscription."""
        mock_subscriber_manager.remove_subscriber.return_value = True
        mock_subscriber_manager.count.return_value = 0

        response = client.post(
            "/api/unsubscribe",
            data=json.dumps({"email": "test@example.com"}),
            content_type="application/json",
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True

    def test_unsubscribe_not_found(self, client, mock_subscriber_manager):
        """Test unsubscribe with non-existent email."""
        mock_subscriber_manager.remove_subscriber.return_value = False

        response = client.post(
            "/api/unsubscribe",
            data=json.dumps({"email": "test@example.com"}),
            content_type="application/json",
        )

        assert response.status_code == 404
        data = json.loads(response.data)
        assert data["success"] is False

    def test_get_subscribers(self, client, mock_subscriber_manager):
        """Test getting all subscribers."""
        mock_subscriber_manager.get_subscribers.return_value = [
            "user1@example.com",
            "user2@example.com",
        ]

        response = client.get("/api/subscribers")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert len(data["subscribers"]) == 2
        assert data["count"] == 2

    def test_send_email_success(
        self, client, mock_subscriber_manager, mock_email_sender
    ):
        """Test successful email sending."""
        mock_subscriber_manager.get_subscribers.return_value = ["user@example.com"]

        from mailer.email_sender import EmailResult

        mock_email_sender.send_email.return_value = EmailResult(
            success=True, message="Sent successfully", failed_recipients=[]
        )

        response = client.post(
            "/api/send-email",
            data=json.dumps({"subject": "Test", "body": "Hello", "html": False}),
            content_type="application/json",
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True

    def test_send_email_no_subscribers(self, client, mock_subscriber_manager):
        """Test sending email with no subscribers."""
        mock_subscriber_manager.get_subscribers.return_value = []

        response = client.post(
            "/api/send-email",
            data=json.dumps({"subject": "Test", "body": "Hello"}),
            content_type="application/json",
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["success"] is False

    def test_send_email_missing_data(self, client):
        """Test sending email without required fields."""
        response = client.post(
            "/api/send-email",
            data=json.dumps({"subject": "Test"}),
            content_type="application/json",
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["success"] is False
