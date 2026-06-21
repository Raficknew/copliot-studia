# GitHub Copilot Instructions - Mailer Project

## 1. Python i Zależności

### Wersja Python
- Używaj Python 3.9+
- Wszystkie funkcje muszą być kompatybilne z Python 3.9

### Formatowanie i Linting
- Przestrzegaj PEP 8 ściśle
- Używaj `black` do automatycznego formatowania
- Używaj `pylint` do sprawdzania jakości kodu (min. 9.0/10)
- Type hints obowiązkowe dla wszystkich funkcji publicznych

### Zarządzanie Zależnościami
- `requirements.txt` zawsze aktualny
- Pinuj wersje dependencies dla reprodukowalności
- Dokumentuj powód dodania każdej nowej zależności

## 2. Struktura Kodu

### Organizacja Modułów
- Moduły: max 500 linii kodu
- Funkcje: max 50 linii
- Klasy: odpowiadają pojedynczej odpowiedzialności (Single Responsibility Principle)
- Separacja concerns: logika biznesowa oddzielona od UI

### Konwencje Nazewnicze
- Funkcje i zmienne: `snake_case`
- Klasy: `PascalCase`
- Stałe: `UPPER_SNAKE_CASE`
- Prywatne metody: prefix `_`
- Pliki modułów: `lowercase_with_underscores.py`

### Dokumentacja
- Dokumentuj w formacie Google Docstring
- Każda funkcja publiczna musi mieć docstring
- Docstring zawiera: opis, Args, Returns, Raises
- Przykłady użycia w docstrings dla złożonych funkcji

### Przykład Standardowej Funkcji
```python
def process_subscriber(email: str, name: Optional[str] = None) -> Dict[str, Any]:
    """Process and validate subscriber information.
    
    Args:
        email: Email address of the subscriber
        name: Optional name of the subscriber
        
    Returns:
        Dictionary containing processed subscriber data
        
    Raises:
        ValueError: If email format is invalid
    """
    # Implementation
    pass
```

## 3. Testowanie

### Wymagania Coverage
- Minimum 80% code coverage (cel: 90%+)
- pytest + pytest-cov do generowania raportów
- Każda funkcja publiczna musi mieć co najmniej 2 testy

### Framework i Narzędzia
- Używaj `pytest` jako głównego frameworka
- `pytest-mock` do mockowania
- `unittest.mock` dla mockowania SMTP i zewnętrznych serwisów
- Fixtures dla reużywalnego setup kodu

### Struktura Testów
- Testy w katalogu `tests/` odzwierciedlają strukturę `mailer/`
- Nazwa pliku testowego: `test_<module_name>.py`
- Nazwa klasy testowej: `Test<ClassName>`
- Nazwa testu: `test_<function>_<scenario>_<expected>`

### Wzorzec Testowy
```python
import pytest
from unittest.mock import Mock, patch

class TestEmailSender:
    @pytest.fixture
    def email_sender(self):
        """Create EmailSender instance for testing."""
        return EmailSender(smtp_server="test.smtp.com")
    
    def test_send_email_success(self, email_sender):
        """Test successful email sending."""
        # Arrange, Act, Assert pattern
        pass
    
    def test_send_email_invalid_recipient_raises_error(self, email_sender):
        """Test error handling for invalid recipient."""
        with pytest.raises(ValueError):
            email_sender.send("invalid-email", "Subject", "Body")
```

### Test Coverage dla Komponentów
- **Email Validation**: format, edge cases, special characters
- **Email Sending**: success, failure, partial failure, SMTP errors
- **Subscriber Management**: CRUD operations, duplicates, persistence
- **Web Routes**: wszystkie endpoints, error codes, validation

### Mockowanie
- Mock SMTP server dla testów email sending
- Mock filesystem dla testów subscriber persistence
- Izoluj testy - żadne realne połączenia sieciowe
- Używaj fixtures do shared mocks

## 4. Bezpieczeństwo

### Credentials i Secrets
- **NIGDY** nie commituj credentials do repozytorium
- Używaj environment variables dla wszystkich secrets
- Plik `.env.example` jako template (bez wartości)
- Dodaj `.env` do `.gitignore`

### Input Validation
- Waliduj wszystkie dane wejściowe od użytkownika
- Email validation: RFC 5322 compliant pattern
- Sanityzuj input przed zapisem do storage
- Escape HTML w output dla zapobiegania XSS

### SMTP i Email Security
- Używaj TLS dla połączeń SMTP
- Timeout dla połączeń SMTP (domyślnie 30s)
- Obsłuż rate limiting dla email sending
- Log failed attempts bez ujawniania credentials

### Przykład Bezpiecznej Konfiguracji
```python
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# Never:
# SMTP_PASSWORD = "hardcoded_password"  # ❌ WRONG
```

## 5. Architektura

### Warstwa Web (Flask)
- MVC pattern dla struktury aplikacji
- Routes w `web.py`
- Logika biznesowa w osobnych modułach
- Dependency Injection gdzie możliwe

### Separacja Concerns
- `validators.py` - tylko walidacja
- `subscribers.py` - tylko zarządzanie subskrybentami
- `email_sender.py` - tylko wysyłanie emaili
- `web.py` - tylko routing i HTTP handling

### Error Handling
- Używaj custom exceptions gdzie sensowne
- Nie łap generycznego `Exception` bez potrzeby
- Zawsze log exceptions z kontekstem
- Zwracaj sensowne HTTP status codes

### Przykład Struktury
```python
# web.py - routing only
@app.route("/api/subscribe", methods=["POST"])
def subscribe():
    data = request.get_json()
    
    # Validation
    if not EmailValidator.validate(data["email"]):
        return jsonify({"error": "Invalid email"}), 400
    
    # Business logic
    result = subscriber_manager.add_subscriber(data["email"])
    
    # Response
    return jsonify({"success": True}), 201
```

## 6. Git i Version Control

### Konwencje Commitów
- Format: `JIRA-ID: Brief description`
- Używaj imperative mood ("Add feature" nie "Added feature")
- Max 72 znaki w pierwszej linii
- Pusta linia przed szczegółowym opisem
- Szczegółowy opis z bullet points

### Przykład Commita
```
JIRA-1234: Add email validation for subscribers

Detailed changes:
- Implemented RFC 5322 compliant validation
- Added comprehensive test coverage
- Updated documentation
```

### Branch Naming
- Feature branches: `feature/JIRA-123-short-description`
- Bug fixes: `bugfix/JIRA-456-issue-name`
- Documentation: `docs/update-readme`
- Hotfixes: `hotfix/critical-issue`

### Pull Requests
- PRs muszą zawierać opis zmian
- Wszystkie testy muszą przechodzić
- Code review wymagany przed merge
- Squash commits przed merge do main

## 7. Komponenty Projektu

### mailer/ - Logika Biznesowa
- Moduły core aplikacji
- Każdy moduł ma jasno określoną odpowiedzialność
- Type hints i docstrings obowiązkowe
- Maksymalna testability

### templates/ - Flask HTML
- Jinja2 templates
- Semantic HTML5
- Accessibility compliant
- Mobile-responsive design

### static/ - CSS i JavaScript
- Organized structure (css/, js/, images/)
- Modern CSS (flexbox, grid)
- Vanilla JavaScript preferowane
- Minify dla production

### tests/ - Testy Jednostkowe
- Mirror structure of mailer/
- Comprehensive coverage
- Fast execution (<1s dla całego suite)
- Isolated tests (no shared state)

## 8. Obsługa Błędów

### Wzorce Error Handling
```python
# Good
def add_subscriber(email: str) -> bool:
    """Add subscriber with proper error handling."""
    try:
        validated = EmailValidator.sanitize(email)
        if not validated:
            raise ValueError(f"Invalid email: {email}")
        
        # Process...
        return True
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise
    except IOError as e:
        logger.error(f"Storage error: {e}")
        return False
```

### HTTP Error Responses
- 200: Success
- 201: Created
- 400: Bad Request (validation error)
- 404: Not Found
- 409: Conflict (duplicate)
- 500: Internal Server Error

## 9. Performance

### Best Practices
- Bulk operations gdzie możliwe
- Connection pooling dla SMTP
- Cache expensive operations
- Lazy loading where appropriate

### Monitoring
- Log important operations
- Track email sending success/failure rates
- Monitor API response times
- Storage size management

## 10. Dokumentacja

### README.md
- Project overview
- Setup instructions
- Usage examples
- API documentation
- Contributing guidelines

### Inline Comments
- Wyjaśniaj "dlaczego", nie "co"
- Komentuj złożoną logikę
- TODO comments z JIRA tickets
- Keep comments up to date

### API Documentation
- Wszystkie endpoints dokumentowane
- Request/response examples
- Error codes explained
- Authentication requirements

## 11. Copilot Skills Integration

### Dostępne Skills
- `email-validation` - Dla walidacji emaili
- `mailer-complete-testing` - Dla kompletnego testowania
- `git-commit-jira` - Dla formatowania commitów

### Użycie Skills
Zamiast pisać kod od zera, pytaj:
```
Use email-validation skill to create validator
Use mailer-complete-testing skill for test template
```

## 12. Continuous Integration

### Pre-commit Checks
```bash
# Before every commit:
./format.sh   # Format code
./lint.sh     # Check quality
./test.sh     # Run tests
```

### CI Pipeline Expectations
1. Run all tests
2. Check code coverage (min 80%)
3. Lint code (min 9.0/10)
4. Build documentation
5. Security scan

## Summary

Te instrukcje zapewniają:
- ✅ Konsystentny kod style
- ✅ Wysoka jakość kodu
- ✅ Bezpieczeństwo
- ✅ Testability
- ✅ Maintainability
- ✅ Dokumentacja

**Zawsze stosuj te standardy dla projektu Mailer.**
