"""Tests for Flask web application."""

import pytest
from flask.testing import FlaskClient
from mailer.web import app, subscriber_manager


@pytest.fixture
def client() -> FlaskClient:
    """Create Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
    # Clean up after each test
    subscriber_manager.clear_subscribers()


class TestWebRoutes:
    """Test suite for web routes."""

    def test_index_route(self, client: FlaskClient) -> None:
        """Test index route returns 200."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"Mailer" in response.data

    def test_subscribe_api_success(self, client: FlaskClient) -> None:
        """Test successful subscription via API."""
        response = client.post(
            "/api/subscribe",
            json={"email": "test@example.com"},
            content_type="application/json",
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert data["success"] is True
        assert "Subscribed successfully" in data["message"]

    def test_subscribe_api_invalid_email(self, client: FlaskClient) -> None:
        """Test subscription with invalid email format."""
        response = client.post(
            "/api/subscribe",
            json={"email": "invalid@"},
            content_type="application/json",
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "Invalid email format" in data["message"]

    def test_subscribe_api_duplicate_email(self, client: FlaskClient) -> None:
        """Test subscription with already subscribed email."""
        client.post(
            "/api/subscribe",
            json={"email": "test@example.com"},
            content_type="application/json",
        )
        
        response = client.post(
            "/api/subscribe",
            json={"email": "test@example.com"},
            content_type="application/json",
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "already subscribed" in data["message"]

    def test_subscribe_api_missing_email(self, client: FlaskClient) -> None:
        """Test subscription without email field."""
        response = client.post(
            "/api/subscribe", json={}, content_type="application/json"
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False

    def test_unsubscribe_api_success(self, client: FlaskClient) -> None:
        """Test successful unsubscribe via API."""
        client.post(
            "/api/subscribe",
            json={"email": "test@example.com"},
            content_type="application/json",
        )
        
        response = client.post(
            "/api/unsubscribe",
            json={"email": "test@example.com"},
            content_type="application/json",
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True

    def test_unsubscribe_api_not_found(self, client: FlaskClient) -> None:
        """Test unsubscribe with email not in list."""
        response = client.post(
            "/api/unsubscribe",
            json={"email": "notfound@example.com"},
            content_type="application/json",
        )
        
        assert response.status_code == 404
        data = response.get_json()
        assert data["success"] is False

    def test_get_subscribers_api(self, client: FlaskClient) -> None:
        """Test getting subscriber list via API."""
        client.post(
            "/api/subscribe",
            json={"email": "test1@example.com"},
            content_type="application/json",
        )
        client.post(
            "/api/subscribe",
            json={"email": "test2@example.com"},
            content_type="application/json",
        )
        
        response = client.get("/api/subscribers")
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert data["count"] == 2
        assert len(data["subscribers"]) == 2

    def test_send_email_api_success(self, client: FlaskClient) -> None:
        """Test sending email to subscribers via API."""
        client.post(
            "/api/subscribe",
            json={"email": "test@example.com"},
            content_type="application/json",
        )
        
        response = client.post(
            "/api/send-email",
            json={"subject": "Test", "body": "Test message"},
            content_type="application/json",
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True

    def test_send_email_api_no_subscribers(self, client: FlaskClient) -> None:
        """Test sending email when no subscribers exist."""
        response = client.post(
            "/api/send-email",
            json={"subject": "Test", "body": "Test message"},
            content_type="application/json",
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "No subscribers" in data["message"]

    def test_send_email_api_missing_fields(self, client: FlaskClient) -> None:
        """Test sending email without required fields."""
        response = client.post(
            "/api/send-email", json={"subject": "Test"}, content_type="application/json"
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False

    def test_404_error_handler(self, client: FlaskClient) -> None:
        """Test 404 error handler returns JSON."""
        response = client.get("/nonexistent")
        
        assert response.status_code == 404
        data = response.get_json()
        assert data["success"] is False
        assert "not found" in data["message"].lower()
