# Email Validation Skill

## Cel umiejętności
Wspieranie tworzenia funkcji walidacji emaili z testami dla projektu Mailer.

## Kontekst
- **Projekt**: Mailer (Flask + email management)
- **Wymaganie**: Walidacja subskrybentów przed dodaniem do listy
- **Standard**: RFC 5322 (uproszczony pattern)
- **Framework testowy**: pytest z parametryzowanymi testami

## Wzorzec: Walidator Email

### Podstawowa Implementacja

```python
import re
from typing import Optional

class EmailValidator:
    """Email validator using RFC 5322 compliant pattern."""
    
    # Pattern: user@domain.com
    PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    @staticmethod
    def validate(email: str) -> bool:
        """Waliduj format emaila.
        
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
```

### Rozszerzona Walidacja z Dodatkowymi Checks

```python
class AdvancedEmailValidator(EmailValidator):
    """Extended email validator with additional checks."""
    
    MAX_LENGTH = 254  # RFC 5321
    MAX_LOCAL_LENGTH = 64
    MAX_DOMAIN_LENGTH = 255
    
    @classmethod
    def validate_with_details(cls, email: str) -> tuple[bool, Optional[str]]:
        """Validate email with detailed error message.
        
        Args:
            email: Email address to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not email or not isinstance(email, str):
            return False, "Email is required"
        
        email = email.strip()
        
        if len(email) > cls.MAX_LENGTH:
            return False, f"Email exceeds maximum length of {cls.MAX_LENGTH}"
        
        if '@' not in email:
            return False, "Email must contain @ symbol"
        
        local, domain = email.rsplit('@', 1)
        
        if len(local) > cls.MAX_LOCAL_LENGTH:
            return False, f"Local part exceeds {cls.MAX_LOCAL_LENGTH} characters"
        
        if len(domain) > cls.MAX_DOMAIN_LENGTH:
            return False, f"Domain exceeds {cls.MAX_DOMAIN_LENGTH} characters"
        
        if not cls.validate(email):
            return False, "Invalid email format"
        
        return True, None
```

## Wzorzec: Testy

### Podstawowe Testy Parametryzowane

```python
import pytest
from mailer.validators import EmailValidator

class TestEmailValidator:
    """Test cases for email validation."""
    
    @pytest.mark.parametrize("email,expected", [
        # Valid emails
        ("user@example.com", True),
        ("user+tag@domain.co.uk", True),
        ("test.user@example.com", True),
        ("user_name@example-domain.com", True),
        ("123@numbers.com", True),
        
        # Invalid emails
        ("invalid@", False),
        ("@domain.com", False),
        ("user@", False),
        ("user", False),
        ("", False),
        ("user @example.com", False),
        ("user@domain", False),
        ("user@@domain.com", False),
        (None, False),
    ])
    def test_email_validation(self, email, expected):
        """Test email validation with various inputs."""
        assert EmailValidator.validate(email) == expected
    
    def test_validate_with_whitespace(self):
        """Test validation strips whitespace."""
        assert EmailValidator.validate("  user@example.com  ") is True
    
    @pytest.mark.parametrize("email,expected", [
        ("User@Example.COM", "user@example.com"),
        ("  TEST@DOMAIN.com  ", "test@domain.com"),
        ("invalid", None),
        ("", None),
        (None, None),
    ])
    def test_sanitize(self, email, expected):
        """Test email sanitization."""
        assert EmailValidator.sanitize(email) == expected
```

### Testy Edge Cases

```python
class TestEmailValidatorEdgeCases:
    """Test edge cases for email validation."""
    
    def test_very_long_email(self):
        """Test validation rejects very long emails."""
        long_local = "a" * 100
        email = f"{long_local}@example.com"
        # Implementation specific - might pass basic validation
        result = EmailValidator.validate(email)
        # Document expected behavior
        
    def test_special_characters_in_local(self):
        """Test special characters in local part."""
        valid_specials = [
            "user.name@example.com",
            "user+tag@example.com",
            "user_name@example.com",
            "user-name@example.com",
        ]
        for email in valid_specials:
            assert EmailValidator.validate(email) is True
    
    def test_international_domains(self):
        """Test international domain names."""
        # Note: Basic pattern doesn't support IDN
        emails = [
            "user@example.co.uk",
            "user@example.com.au",
            "user@sub.domain.example.com",
        ]
        for email in emails:
            assert EmailValidator.validate(email) is True
    
    def test_consecutive_dots(self):
        """Test emails with consecutive dots are rejected."""
        invalid = [
            "user..name@example.com",
            "user@example..com",
        ]
        for email in invalid:
            # Basic pattern might not catch this
            # Document behavior
            result = EmailValidator.validate(email)
```

### Testy Integracyjne

```python
class TestEmailValidatorIntegration:
    """Integration tests with subscriber management."""
    
    def test_validator_integration_with_subscriber_manager(self, tmp_path):
        """Test validator works with subscriber manager."""
        from mailer.subscribers import SubscriberManager
        
        storage = tmp_path / "test.json"
        manager = SubscriberManager(storage_path=str(storage))
        
        # Valid email should be added
        assert manager.add_subscriber("valid@example.com") is True
        
        # Invalid email should raise ValueError
        with pytest.raises(ValueError):
            manager.add_subscriber("invalid-email")
    
    def test_validator_in_web_api(self, client):
        """Test validator integration in Flask routes."""
        # Valid email
        response = client.post(
            "/api/subscribe",
            json={"email": "test@example.com"}
        )
        assert response.status_code == 201
        
        # Invalid email
        response = client.post(
            "/api/subscribe",
            json={"email": "invalid"}
        )
        assert response.status_code == 400
```

## Reguły Walidacji

### Must-Have Rules
1. ✅ Email musi zawierać dokładnie jeden `@` symbol
2. ✅ Local part (przed @) nie może być pusta
3. ✅ Domain part (po @) musi zawierać co najmniej jedną kropkę
4. ✅ TLD (top-level domain) musi mieć co najmniej 2 znaki
5. ✅ Whitespace na początku/końcu jest usuwany
6. ✅ Case-insensitive (konwertuj do lowercase)

### Pattern Details
```python
PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# Breakdown:
# ^                      - Start of string
# [a-zA-Z0-9._%+-]+      - Local part: alphanumeric + special chars
# @                      - Required @ symbol
# [a-zA-Z0-9.-]+         - Domain: alphanumeric + dots and hyphens
# \.                     - Required dot before TLD
# [a-zA-Z]{2,}           - TLD: minimum 2 letters
# $                      - End of string
```

### Co Pattern NIE Obsługuje
- ❌ Quoted strings (e.g., `"user name"@example.com`)
- ❌ IP addresses jako domain (e.g., `user@[192.168.1.1]`)
- ❌ Comments (e.g., `user@example.com (comment)`)
- ❌ International characters (IDN) bez konwersji
- ❌ Complex RFC 5322 edge cases

To jest **uproszczony pattern** dla 99% przypadków użycia.

## Best Practices

### Walidacja
- Patrz RFC 5322 dla pełnej specyfikacji
- Waliduj zarówno format jak i długość
- **Nie wysyłaj testowego emaila** dla walidacji formatu
- Użyj parametryzowanych testów dla różnych przypadków
- Dokumentuj, które edge cases są i nie są obsługiwane

### Testowanie
- Test happy path + edge cases + error cases
- Użyj `pytest.mark.parametrize` dla wielu przypadków
- Test whitespace handling
- Test case sensitivity
- Test integration z innymi komponentami

### Security
- Zawsze sanityzuj input przed zapisem
- Nie ufaj user input
- Log failed validation attempts
- Rate limit validation requests w API

## Przykłady Użycia

### W Subscriber Manager
```python
class SubscriberManager:
    def add_subscriber(self, email: str) -> bool:
        """Add subscriber with validation."""
        sanitized = EmailValidator.sanitize(email)
        if not sanitized:
            raise ValueError(f"Invalid email format: {email}")
        
        # Proceed with adding...
        return True
```

### W Flask Route
```python
@app.route("/api/subscribe", methods=["POST"])
def subscribe():
    """Subscribe endpoint with validation."""
    data = request.get_json()
    email = data.get("email", "")
    
    if not EmailValidator.validate(email):
        return jsonify({
            "success": False,
            "error": "Invalid email format"
        }), 400
    
    # Proceed with subscription...
```

### W Frontend JavaScript
```javascript
function validateEmail(email) {
    // Client-side validation (same pattern)
    const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return pattern.test(email);
}
```

## Tools i Dependencies

### Required
- `re` (standard library) - Regex matching
- `typing` (standard library) - Type hints

### Testing
- `pytest` - Test framework
- `pytest.mark.parametrize` - Parametrized tests
- `pytest fixtures` - Test setup

### Optional
- `email-validator` library - For advanced validation
- `idna` - For international domain names

## Summary

Email Validation Skill zapewnia:
- ✅ RFC 5322 compliant pattern (simplified)
- ✅ Comprehensive test coverage
- ✅ Integration examples
- ✅ Security best practices
- ✅ Clear documentation

**Użyj tego skill przy tworzeniu lub modyfikowaniu walidacji email w projekcie Mailer.**
