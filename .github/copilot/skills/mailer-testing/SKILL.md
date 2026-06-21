# Mailer Complete Testing Skill

## Cel
Kompleksowe wsparcie dla testowania wszystkich komponentów projektu Mailer przy użyciu pytest, mockowania i najlepszych praktyk testowych.

## Komponenty do Testowania

### 1. Email Validation
Testowanie walidacji formatów email:
- ✅ Format email (RFC 5322)
- ✅ Długość emaila
- ✅ Special characters (+, ., _, -, %)
- ✅ Case sensitivity
- ✅ Whitespace handling
- ✅ Edge cases (None, empty, invalid)

### 2. Email Sending
Testowanie wysyłania emaili z mockowaniem SMTP:
- ✅ Single recipient
- ✅ Multiple recipients
- ✅ HTML vs Plain text
- ✅ Error handling (SMTP errors)
- ✅ Partial failures
- ✅ Timeout handling
- ✅ Authentication errors

### 3. Subscribers Management
Testowanie zarządzania subskrybentami:
- ✅ Add subscriber (success, duplicate)
- ✅ Remove subscriber (success, not found)
- ✅ List subscribers
- ✅ Count subscribers
- ✅ Duplicate prevention
- ✅ Persistence (save/load from JSON)
- ✅ Case insensitive handling

### 4. Web Interface (Flask)
Testowanie routów Flask i API:
- ✅ Routes accessibility (200, 404)
- ✅ Form validation
- ✅ Error handling (400, 500)
- ✅ JSON request/response
- ✅ HTTP status codes
- ✅ HTML rendering

## Test Template

### Podstawowy Template dla Komponentu

```python
import pytest
from unittest.mock import Mock, patch, MagicMock
from mailer.email_sender import EmailSender
from mailer.subscribers import SubscriberManager

class TestMailerComponent:
    """Test suite for Mailer component."""
    
    @pytest.fixture
    def component_setup(self):
        """Setup fixture for component tests.
        
        Returns:
            Initialized component instance
        """
        # Setup test environment
        component = ComponentClass(test_config)
        yield component
        # Teardown
        component.cleanup()
    
    def test_happy_path(self, component_setup):
        """Test main success scenario."""
        # Arrange
        input_data = "valid_input"
        expected_output = "expected_result"
        
        # Act
        result = component_setup.process(input_data)
        
        # Assert
        assert result == expected_output
    
    def test_edge_cases(self, component_setup):
        """Test boundary conditions and edge cases."""
        edge_cases = [
            (None, None),
            ("", ""),
            ("extreme_value", "extreme_result"),
        ]
        
        for input_val, expected in edge_cases:
            result = component_setup.process(input_val)
            assert result == expected
    
    def test_error_handling(self, component_setup):
        """Test error scenarios and exception handling."""
        with pytest.raises(ValueError):
            component_setup.process("invalid_input")
```

## Szczegółowe Przykłady Testów

### Email Sender Tests

```python
import pytest
from unittest.mock import Mock, patch, MagicMock
from mailer.email_sender import EmailSender, EmailResult

@pytest.fixture
def email_sender():
    """Create EmailSender for testing."""
    return EmailSender(
        smtp_server="smtp.test.com",
        smtp_port=587,
        smtp_username="test@test.com",
        smtp_password="password",
    )

class TestEmailSender:
    """Comprehensive email sender tests."""
    
    @patch("mailer.email_sender.smtplib.SMTP")
    def test_send_email_single_recipient_success(
        self, mock_smtp, email_sender
    ):
        """Test successful email to single recipient."""
        # Arrange
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        # Act
        result = email_sender.send_email(
            ["user@example.com"], "Test", "Body"
        )
        
        # Assert
        assert result.success is True
        assert len(result.failed_recipients) == 0
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once()
        assert mock_server.send_message.call_count == 1
    
    @patch("mailer.email_sender.smtplib.SMTP")
    def test_send_email_multiple_recipients(
        self, mock_smtp, email_sender
    ):
        """Test email to multiple recipients."""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        recipients = ["user1@example.com", "user2@example.com"]
        result = email_sender.send_email(recipients, "Test", "Body")
        
        assert result.success is True
        assert mock_server.send_message.call_count == len(recipients)
    
    @patch("mailer.email_sender.smtplib.SMTP")
    def test_send_email_partial_failure(
        self, mock_smtp, email_sender
    ):
        """Test partial failure when sending to multiple recipients."""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        # First send succeeds, second fails
        mock_server.send_message.side_effect = [
            None,
            Exception("SMTP error")
        ]
        
        recipients = ["user1@example.com", "user2@example.com"]
        result = email_sender.send_email(recipients, "Test", "Body")
        
        assert result.success is False
        assert len(result.failed_recipients) == 1
        assert "user2@example.com" in result.failed_recipients
    
    @patch("mailer.email_sender.smtplib.SMTP")
    def test_send_email_smtp_connection_error(
        self, mock_smtp, email_sender
    ):
        """Test SMTP connection failure handling."""
        mock_smtp.side_effect = Exception("Connection refused")
        
        result = email_sender.send_email(
            ["user@example.com"], "Test", "Body"
        )
        
        assert result.success is False
        assert "SMTP error" in result.message
    
    def test_send_email_no_recipients(self, email_sender):
        """Test sending with empty recipients list."""
        result = email_sender.send_email([], "Test", "Body")
        
        assert result.success is False
        assert "No recipients" in result.message
```

### Subscriber Manager Tests

```python
import pytest
import tempfile
import os
from mailer.subscribers import SubscriberManager

@pytest.fixture
def temp_storage():
    """Create temporary storage file."""
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)

@pytest.fixture
def manager(temp_storage):
    """Create SubscriberManager with temp storage."""
    return SubscriberManager(storage_path=temp_storage)

class TestSubscriberManager:
    """Comprehensive subscriber management tests."""
    
    def test_add_subscriber_success(self, manager):
        """Test adding new subscriber."""
        result = manager.add_subscriber("user@example.com")
        
        assert result is True
        assert manager.count() == 1
        assert "user@example.com" in manager.get_subscribers()
    
    def test_add_subscriber_duplicate_returns_false(self, manager):
        """Test adding duplicate subscriber."""
        manager.add_subscriber("user@example.com")
        result = manager.add_subscriber("user@example.com")
        
        assert result is False
        assert manager.count() == 1
    
    def test_add_subscriber_case_insensitive(self, manager):
        """Test case insensitive duplicate detection."""
        manager.add_subscriber("User@Example.COM")
        result = manager.add_subscriber("user@example.com")
        
        assert result is False
        assert manager.count() == 1
    
    def test_add_subscriber_invalid_email_raises(self, manager):
        """Test invalid email raises ValueError."""
        with pytest.raises(ValueError):
            manager.add_subscriber("invalid-email")
    
    def test_remove_subscriber_success(self, manager):
        """Test removing existing subscriber."""
        manager.add_subscriber("user@example.com")
        result = manager.remove_subscriber("user@example.com")
        
        assert result is True
        assert manager.count() == 0
    
    def test_remove_subscriber_not_found(self, manager):
        """Test removing non-existent subscriber."""
        result = manager.remove_subscriber("notfound@example.com")
        
        assert result is False
    
    def test_persistence_across_instances(self, temp_storage):
        """Test data persists across manager instances."""
        # First instance
        manager1 = SubscriberManager(storage_path=temp_storage)
        manager1.add_subscriber("user@example.com")
        
        # Second instance should load the data
        manager2 = SubscriberManager(storage_path=temp_storage)
        assert manager2.count() == 1
        assert "user@example.com" in manager2.get_subscribers()
```

### Flask Web Tests

```python
import pytest
import json
from unittest.mock import patch
from mailer.web import app

@pytest.fixture
def client():
    """Create Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_subscriber_manager():
    """Mock SubscriberManager."""
    with patch("mailer.web.subscriber_manager") as mock:
        yield mock

class TestWebRoutes:
    """Test Flask web routes."""
    
    def test_index_route_returns_200(self, client):
        """Test main page loads successfully."""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_subscribe_api_valid_email(
        self, client, mock_subscriber_manager
    ):
        """Test subscribe API with valid email."""
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
    
    def test_subscribe_api_invalid_email(self, client):
        """Test subscribe API rejects invalid email."""
        response = client.post(
            "/api/subscribe",
            data=json.dumps({"email": "invalid-email"}),
            content_type="application/json",
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["success"] is False
        assert "Invalid email" in data["error"]
    
    def test_subscribe_api_missing_email(self, client):
        """Test subscribe API requires email field."""
        response = client.post(
            "/api/subscribe",
            data=json.dumps({}),
            content_type="application/json",
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["success"] is False
```

## Coverage Requirements

### Target Coverage Metrics
- **Functions**: 100% (wszystkie funkcje testowane)
- **Branches**: 80%+ (wszystkie główne ścieżki)
- **Lines**: 85%+ (comprehensive coverage)
- **Overall**: 90%+ (cel końcowy)

### Coverage Command
```bash
pytest --cov=mailer --cov-report=html --cov-report=term
```

### Coverage Report Interpretation
```
Name                     Stmts   Miss  Cover
--------------------------------------------
mailer/__init__.py           2      0   100%
mailer/email_sender.py      51      0   100%
mailer/subscribers.py       47      2    96%
mailer/validators.py        15      0   100%
mailer/web.py               62      8    87%
--------------------------------------------
TOTAL                      177     10    94%
```

## Tools i Best Practices

### Testing Tools
- **pytest** - Główny framework testowy
- **pytest-cov** - Coverage reporting
- **pytest-mock** - Mocking utilities
- **unittest.mock** - Python standard mocking
- **pytest fixtures** - Reusable test setup

### Mocking Strategy
```python
# Mock external services
@patch("mailer.email_sender.smtplib.SMTP")
def test_with_mocked_smtp(mock_smtp):
    pass

# Mock file I/O
@patch("builtins.open", mock_open(read_data="data"))
def test_with_mocked_file():
    pass

# Mock environment variables
@patch.dict(os.environ, {"SMTP_SERVER": "test.smtp.com"})
def test_with_env_vars():
    pass
```

### Fixtures Best Practices
```python
# Use fixtures for setup/teardown
@pytest.fixture
def setup_data():
    # Setup
    data = create_test_data()
    yield data
    # Teardown
    cleanup_test_data(data)

# Use fixtures for dependency injection
@pytest.fixture
def email_sender():
    return EmailSender(smtp_server="test.smtp.com")
```

### Parametrized Tests
```python
@pytest.mark.parametrize("input,expected", [
    ("valid", True),
    ("invalid", False),
    ("edge_case", None),
])
def test_with_parameters(input, expected):
    assert process(input) == expected
```

## Summary

Mailer Complete Testing Skill zapewnia:
- ✅ Comprehensive test patterns dla wszystkich komponentów
- ✅ Mocking strategies dla external dependencies
- ✅ Coverage targets i reporting
- ✅ Best practices dla pytest i fixtures
- ✅ Integration testing patterns

**Użyj tego skill przy tworzeniu lub rozszerzaniu testów w projekcie Mailer.**
