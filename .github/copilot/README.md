# GitHub Copilot Configuration for Mailer

Kompleksowa konfiguracja GitHub Copilot dla projektu Mailer, zawierająca instrukcje globalne, skills specjalistyczne oraz agentów autonomicznych.

---

## 📋 Struktura

```
.github/
├── copilot/
│   ├── README.md                      # Ten plik
│   └── skills/                        # Pakiety specjalistycznej wiedzy
│       ├── email-validation/          # Walidacja adresów email
│       ├── mailer-testing/            # Kompleksowe testowanie
│       └── email-templates/           # Zarządzanie szablonami email
│
└── agents/                            # Autonomiczne agenty
    ├── docs-generator-agent.yaml      # Generator dokumentacji
    └── docs-generator-workflow.md     # Workflow agenta

.kiro/skills/git-commit-jira/          # Formatowanie commitów (Kiro-specific)

copilot-instructions.md                # Globalne standardy projektu (root)
```

---

## 📚 Instrukcje (Instructions)

### copilot-instructions.md

**Lokalizacja:** Katalog główny projektu

**Cel:** Globalne standardy kodowania dla całego projektu Mailer

**Zawartość:**
- Python 3.9+ requirements
- PEP 8 compliance
- Type hints i Google Docstrings
- Testing requirements (80% coverage)
- Security best practices
- Git commit conventions
- Architecture patterns (MVC, DI)

**Kiedy używać:**
- Zawsze podczas pisania nowego kodu
- Przed code review
- Podczas refactoringu

**Przykład:**
```python
# Zgodnie z instructions:
def process_subscriber(email: str) -> bool:
    """Process subscriber with validation.
    
    Args:
        email: Email address to process
        
    Returns:
        True if processed successfully
        
    Raises:
        ValueError: If email format invalid
    """
    # Implementation following PEP 8
    pass
```

---

## 🎓 Skills (Umiejętności)

### 1. email-validation

**Lokalizacja:** `.github/copilot/skills/email-validation/`

**Opis:** Wsparcie dla walidacji adresów email z RFC 5322 compliance

**Topics:** validation, email, regex, testing

**Zastosowanie:**
- `**/validators/**` - Pliki walidatorów
- `**/test_*validators*` - Testy walidacji
- `**/test_*subscribers*` - Testy subskrybentów

**Funkcje:**
- RFC 5322 compliant regex pattern
- Email sanitization (lowercase, trim)
- Comprehensive test patterns
- Edge cases handling

**Użycie:**
```
@copilot use email-validation skill

// lub
"Create email validator using email-validation skill"
```

**Przykładowy output:**
```python
class EmailValidator:
    PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    @staticmethod
    def validate(email: str) -> bool:
        """Validate email format."""
        if not email or not isinstance(email, str):
            return False
        return bool(re.match(EmailValidator.PATTERN, email.strip()))
```

---

### 2. mailer-complete-testing

**Lokalizacja:** `.github/copilot/skills/mailer-testing/`

**Opis:** Kompleksowy skill dla testowania wszystkich komponentów Mailer

**Topics:** testing, pytest, email, flask, validation, mocking

**Zastosowanie:**
- `**/tests/**` - Wszystkie pliki testowe
- `**/test_*.py` - Pliki testów

**Komponenty testowane:**
- Email validation (format, edge cases)
- Email sending (SMTP, failures, partial)
- Subscriber management (CRUD, persistence)
- Web interface (Flask routes, API)

**Funkcje:**
- Test templates z fixtures
- Mocking strategies (SMTP, filesystem)
- Parametrized tests
- Coverage requirements (80%+)

**Użycie:**
```
"Use mailer-complete-testing skill to create test suite"

// lub
@copilot generate tests using mailer-complete-testing
```

**Przykładowy output:**
```python
@pytest.fixture
def email_sender():
    return EmailSender(smtp_server="test.smtp.com")

@patch("mailer.email_sender.smtplib.SMTP")
def test_send_email_success(mock_smtp, email_sender):
    """Test successful email sending."""
    # Full test implementation with mocking
    pass
```

---

### 3. git-commit-jira

**Lokalizacja:** `.kiro/skills/git-commit-jira/`

**Opis:** Formatowanie git commitów z Jira ID i szczegółowym opisem

**Topics:** git, commit, jira, version-control

**Format:**
```
JIRA-ID: Brief summary (imperative, <72 chars)

Detailed description:
- Bullet point 1
- Bullet point 2
- Additional context
```

**Użycie:**
```bash
git commit -m "JIRA-1234: Add email validation" -m "
Detailed changes:
- Implemented RFC 5322 validation
- Added comprehensive tests
- Updated documentation
"
```

---

### 4. email-templates

**Lokalizacja:** `.github/copilot/skills/email-templates/`

**Opis:** Zarządzanie szablonami email (HTML/Plain text) z Jinja2

**Topics:** email, templates, jinja2, html, text-formatting

**Zastosowanie:**
- `**/templates/**` - Pliki szablonów
- `**/email_*.py` - Moduły email
- `**/test_*email*` - Testy emaili

**Funkcje:**
- Template inheritance (base templates)
- Variable substitution
- HTML + Plain text variants
- Reusable partials (header, footer)
- Best practices dla email HTML

**Użycie:**
```
"Create welcome email template using email-templates skill"
```

**Przykładowy output:**
```python
class EmailTemplateManager:
    def render_welcome_email(
        self, user_name: str, user_email: str
    ) -> str:
        """Render welcome email with template."""
        context = {
            'user_name': user_name,
            'user_email': user_email,
        }
        return self.render_template('welcome', context, 'html')
```

---

## 🤖 Agenci (Agents)

### 1. docs-generator-agent

**Lokalizacja:** `.github/agents/docs-generator-agent.yaml`

**Opis:** Autonomiczny agent do automatycznego generowania dokumentacji

**Model:** claude-sonnet-4 (lub dostępny)

**Capabilities:**
- code-analysis
- documentation-generation
- example-creation
- test-analysis

**Activation Triggers:**
- "Generate documentation for [module]"
- "generate docs"
- "create documentation"
- "document this"

**Workflow (5 faz):**
1. **Analysis** - Skanuj kod, ekstrahuj API
2. **Context Gathering** - Przeczytaj testy, dependencies
3. **Generation** - Generuj Markdown docs
4. **Examples** - Twórz usage examples
5. **Validation** - Waliduj completeness

**Output:**
- `docs/api/[module].md` - API reference
- `docs/examples/[module]_usage.md` - Usage examples
- Updated `docs/CHANGELOG.md`

**Użycie:**
```
"Generate API documentation for mailer.subscribers module"

// Agent will:
// 1. Analyze subscribers.py
// 2. Extract docstrings and types
// 3. Generate comprehensive docs
// 4. Create usage examples
// 5. Validate and save
```

**Success Criteria:**
- ✅ Wszystkie funkcje dokumentowane
- ✅ Wszystkie parametry opisane
- ✅ Type hints pokazane
- ✅ Min. 5 examples
- ✅ Markdown valid

**Timeline:** ~30-60 seconds dla standardowego modułu

---

## 🔄 Workflow Projektu

### Typowy Development Flow

```
1. Developer pisze nowy kod
   └─> Copilot sugeruje pattern z odpowiedniego skill
       (np. email-validation dla walidatorów)

2. Developer dodaje funkcję
   └─> Copilot Instructions zapewnia:
       - Type hints
       - Docstring format
       - PEP 8 compliance

3. Developer generuje testy
   └─> Use mailer-complete-testing skill
       - Testy z fixtures
       - Mocking patterns
       - Parametrized cases

4. Developer commituje zmiany
   └─> Use git-commit-jira skill
       - Formatted commit message
       - Jira ID included
       - Detailed description

5. Developer tworzy dokumentację
   └─> Invoke docs-generator-agent
       - Automatic API docs
       - Usage examples
       - Validation
```

### Example Session

```bash
# 1. Write validator
@copilot "use email-validation skill to create validator"

# 2. Generate tests
@copilot "use mailer-complete-testing skill for validator tests"

# 3. Run tests
./test.sh

# 4. Format code
./format.sh

# 5. Commit
git commit -m "JIRA-1234: Add email validator" -m "..."

# 6. Generate docs
@copilot "Generate documentation for mailer.validators module"
```

---

## 🎯 Best Practices

### When to Use Skills

**✅ Use Skills When:**
- Tworzysz nowy komponent w znanej domenie
- Potrzebujesz template kodu lub testu
- Chcesz zachować consistency
- Uczysz się wzorców projektu

**❌ Nie używaj Skills gdy:**
- Piszesz coś całkowicie niestandardowego
- Eksperymentujesz z nowym podejściem
- Prototypujesz szybko

### When to Invoke Agents

**✅ Invoke Agents When:**
- Potrzebujesz complex, multi-step operation
- Automatyzacja repetitive task
- Generowanie dokumentacji dla modułu
- Analiza i refactoring kodu

**❌ Nie invoke Agents dla:**
- Prostych single-step tasks
- Krytycznych decyzji architekturalnych
- Code review (human required)

### Integration Strategy

1. **Start with Instructions** - Zawsze stosuj globalne standardy
2. **Apply Skills** - Używaj skills dla specific tasks
3. **Leverage Agents** - Invoke agents dla automation
4. **Review & Refine** - Human oversight zawsze ważne

---

## 📊 Monitoring & Metrics

### Skill Effectiveness

Mierz skuteczność skills przez:
- Code quality metrics (pylint scores)
- Test coverage percentages
- Time saved in development
- Consistency across codebase

### Agent Performance

Trackuj performance agents:
- Execution time
- Documentation completeness
- Accuracy of generated content
- Developer satisfaction

---

## 🔮 Future Expansions

### Planned Skills
- `flask-routing` - Flask route patterns
- `async-patterns` - Async/await patterns
- `database-integration` - DB operations

### Planned Agents
- `refactoring-agent` - Automated refactoring
- `test-generator-agent` - Comprehensive test generation
- `security-audit-agent` - Security scanning

---

## 📖 Resources

### Documentation
- [GitHub Copilot Docs](https://docs.github.com/en/copilot)
- [Jinja2 Templates](https://jinja.palletsprojects.com/)
- [pytest Documentation](https://docs.pytest.org/)

### Project Files
- `README.md` - Project overview
- `requirements.md` - Original requirements
- `skills-agents-excersize.md` - Exercise guide
- `SETUP.md` - Setup instructions

### External Resources
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [RFC 5322 Email Standard](https://tools.ietf.org/html/rfc5322)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

## 🎓 Learning Path

### For New Developers

1. **Read Instructions** (`copilot-instructions.md`)
2. **Explore Skills** (Browse `.copilot/skills/`)
3. **Try a Skill** (Use email-validation)
4. **Invoke an Agent** (docs-generator)
5. **Create Custom Skill** (For specific need)

### For Advanced Users

1. **Customize Instructions** (Team-specific rules)
2. **Create New Skills** (Domain-specific patterns)
3. **Configure Agents** (Custom workflows)
4. **Integrate with CI/CD** (Automated checks)

---

## ⚙️ Configuration

### Skill Activation

Skills activate automatically based on:
- File path patterns (`applyTo`)
- Topics relevance
- Language detection
- Pattern matching

### Agent Invocation

Agents require explicit trigger:
- Command syntax
- Keywords detection
- Manual invocation

### Customization

Modify `.promptyaml` files to:
- Change activation patterns
- Add new topics
- Adjust language detection
- Configure preferences

---

## 🆘 Troubleshooting

### Skills Not Activating

**Problem:** Skill doesn't activate when expected

**Solutions:**
1. Check `.promptyaml` applyTo patterns
2. Verify file path matches pattern
3. Ensure topics are relevant
4. Restart IDE/Copilot

### Agent Not Responding

**Problem:** Agent doesn't respond to trigger

**Solutions:**
1. Check activation keywords
2. Verify agent configuration file
3. Check model availability
4. Invoke explicitly with full command

### Poor Quality Suggestions

**Problem:** Copilot suggestions don't match standards

**Solutions:**
1. Review Instructions file
2. Check if correct Skill is active
3. Provide more context in comments
4. Refine skill documentation

---

## 📝 Summary

GitHub Copilot Configuration dla Mailer zapewnia:

- ✅ **Instructions** - Globalne standardy (copilot-instructions.md)
- ✅ **4 Skills** - Specjalistyczna wiedza dla specific tasks
- ✅ **1 Agent** - Automatyczna generacja dokumentacji
- ✅ **Workflow Integration** - Seamless development process
- ✅ **Best Practices** - Proven patterns i conventions
- ✅ **Extensibility** - Easy to add new skills/agents

**Główne Benefity:**
- 🚀 Faster development
- 📊 Higher code quality
- 🧪 Better test coverage
- 📖 Comprehensive documentation
- 🤝 Team consistency

---

**Wersja:** 1.0.0  
**Data:** 2026-06-21  
**Projekt:** Mailer Email Management System  
**Zespół:** Kiro AI + Development Team  

---

**Powodzenia z wykorzystaniem GitHub Copilot w projekcie Mailer! 🚀**
