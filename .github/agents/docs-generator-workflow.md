# Workflow: Documentation Generation Agent

## Trigger

```
Użytkownik: "Generate API documentation for mailer.subscribers module"
```

## Execution Flow

### Phase 1: Analysis (10-15s)

**Działania:**
1. Przeczytaj `mailer/subscribers.py`
2. Przeanalizuj strukturę klas i funkcji
3. Wyciągnij docstrings i type hints
4. Identyfikuj eksportowane API (public methods)

**Output Phase 1:**
- Lista wszystkich klas i metod
- Extracted docstrings
- Type signatures
- Dependencies

**Example:**
```python
# Detected:
class SubscriberManager:
    def __init__(self, storage_path: str) -> None
    def add_subscriber(self, email: str) -> bool
    def remove_subscriber(self, email: str) -> bool
    def get_subscribers(self) -> List[str]
    def count(self) -> int
```

### Phase 2: Context Gathering (5-10s)

**Działania:**
1. Przeczytaj `tests/test_subscribers.py`
2. Poszukaj usage patterns w testach
3. Zbierz informacje o zależnościach (imports)
4. Sprawdź README dla kontekstu projektu

**Output Phase 2:**
- Usage examples z testów
- Edge cases covered
- Dependencies map
- Project context

**Example:**
```python
# From tests:
manager = SubscriberManager("subscribers.json")
manager.add_subscriber("user@example.com")  # Returns True
manager.add_subscriber("user@example.com")  # Returns False (duplicate)
```

### Phase 3: Generation (10-20s)

**Działania:**
1. Stwórz strukturę dokumentacji markdown
2. Konwertuj docstrings na sformatowany Markdown
3. Dodaj type hints do każdej sygnatury
4. Generuj tabelę API methods
5. Dodaj opisy parametrów i return values

**Output Phase 3:**
```markdown
# SubscriberManager API

## Class: SubscriberManager

Manages mailing list subscribers with persistent storage.

### Constructor

\`\`\`python
SubscriberManager(storage_path: str = "subscribers.json")
\`\`\`

**Parameters:**
- `storage_path` (str): Path to JSON file for storing subscribers

### Methods

#### add_subscriber

\`\`\`python
def add_subscriber(email: str) -> bool
\`\`\`

Add a new subscriber to the mailing list.

**Parameters:**
- `email` (str): Email address to add

**Returns:**
- `bool`: True if added successfully, False if already exists

**Raises:**
- `ValueError`: If email format is invalid
```

### Phase 4: Examples (15-30s)

**Działania:**
1. Stwórz Basic Usage example (happy path)
2. Dodaj Advanced Usage patterns (multiple operations)
3. Dołącz Error Handling example (exception handling)
4. Utwórz Complete Working Example (end-to-end)

**Output Phase 4:**
```markdown
## Examples

### Basic Usage

\`\`\`python
from mailer.subscribers import SubscriberManager

# Initialize manager
manager = SubscriberManager("subscribers.json")

# Add subscribers
manager.add_subscriber("user1@example.com")
manager.add_subscriber("user2@example.com")

# Get all subscribers
subscribers = manager.get_subscribers()
print(f"Total: {manager.count()}")
\`\`\`

### Advanced Usage

\`\`\`python
# Batch operations
emails = ["user1@example.com", "user2@example.com", "user3@example.com"]
for email in emails:
    try:
        manager.add_subscriber(email)
    except ValueError as e:
        print(f"Invalid email {email}: {e}")

# Check and remove
if manager.count() > 100:
    # Remove oldest or cleanup
    pass
\`\`\`

### Error Handling

\`\`\`python
try:
    manager.add_subscriber("invalid-email")
except ValueError as e:
    print(f"Validation error: {e}")
    
# Check before removing
if "user@example.com" in manager.get_subscribers():
    manager.remove_subscriber("user@example.com")
\`\`\`

### Complete Example

\`\`\`python
#!/usr/bin/env python3
from mailer.subscribers import SubscriberManager

def main():
    # Setup
    manager = SubscriberManager("my_list.json")
    
    # Add multiple subscribers
    new_subscribers = [
        "alice@example.com",
        "bob@example.com",
        "charlie@example.com"
    ]
    
    for email in new_subscribers:
        if manager.add_subscriber(email):
            print(f"✓ Added: {email}")
        else:
            print(f"✗ Already exists: {email}")
    
    # Display summary
    print(f"\nTotal subscribers: {manager.count()}")
    print("All subscribers:")
    for email in manager.get_subscribers():
        print(f"  - {email}")

if __name__ == "__main__":
    main()
\`\`\`
```

### Phase 5: Validation (5-10s)

**Działania:**
1. Waliduj Markdown syntax (lint markdown)
2. Sprawdź completeness (wszystkie metody dokumentowane?)
3. Weryfikuj code snippets (czy przykłady są poprawne syntaktycznie?)
4. Zakończ z summary (raport co zostało wygenerowane)

**Validation Checks:**
- ✅ Wszystkie public methods mają dokumentację
- ✅ Wszystkie parametry są opisane
- ✅ Type hints są pokazane
- ✅ Minimum 5 examples
- ✅ Markdown syntax valid
- ✅ Code snippets są executable
- ✅ Links są poprawne

**Output Phase 5:**
```
✅ Documentation Generation Complete

Files created:
- docs/api/subscribers.md (1,234 words)
- docs/examples/subscribers_usage.md (567 words)

Content summary:
- 1 class documented
- 5 methods documented
- 4 usage examples
- 12 code snippets
- 100% API coverage

Validation results:
✅ Markdown syntax valid
✅ All methods documented
✅ All parameters described
✅ Type hints included
✅ Examples runnable
```

## Final Output Structure

```
docs/
├── api/
│   └── subscribers.md          # API reference
├── examples/
│   └── subscribers_usage.md    # Usage examples
└── CHANGELOG.md                # Updated with changes
```

### docs/api/subscribers.md

```markdown
# SubscriberManager API Reference

## Overview
[Generated overview]

## Class Reference
[Detailed class documentation]

## Methods
[All methods with signatures]

## Exceptions
[All exceptions that can be raised]

## See Also
- [Email Validation](validators.md)
- [Usage Examples](../examples/subscribers_usage.md)
```

### docs/examples/subscribers_usage.md

```markdown
# SubscriberManager Usage Examples

## Table of Contents
1. [Getting Started](#getting-started)
2. [Basic Operations](#basic-operations)
3. [Advanced Patterns](#advanced-patterns)
4. [Error Handling](#error-handling)
5. [Best Practices](#best-practices)

[Detailed examples for each section]
```

## Success Criteria

Dokumentacja jest uznawana za complete gdy:
- ✅ Wszystkie funkcje publiczne dokumentowane
- ✅ Wszystkie parametry opisane z typami
- ✅ Type hints pokazane w sygnaturach
- ✅ Minimum 5 working examples
- ✅ Markdown valid (no syntax errors)
- ✅ Code snippets testowane/executable
- ✅ Links między dokumentami działają
- ✅ Overview i context provided

## Error Handling

### Gdy kod jest niepełny:
```
⚠️ Warning: Incomplete docstrings detected
- Method `process_bulk` missing docstring
- Parameter descriptions missing in `validate`

Recommendation: Add docstrings before generating docs
```

### Gdy testy są missing:
```
⚠️ Warning: No tests found for this module
Usage examples will be synthetic

Recommendation: Write tests for better examples
```

### Gdy dependencies are missing:
```
❌ Error: Cannot analyze module
Import error: No module named 'mailer.validators'

Recommendation: Ensure all dependencies are installed
```

## Agent Memory

Agent pamięta między invocations:
- Project structure
- Previously documented modules
- Naming conventions used
- Documentation style preferences
- Common patterns in codebase

## Customization Options

User może specify:
```
Generate API documentation for mailer.subscribers module
- Include installation instructions
- Add troubleshooting section
- Focus on error handling
- Generate detailed examples
```

Agent dostosuje output based on requirements.

## Timeline Example

```
[00:00] Starting documentation generation...
[00:02] Phase 1: Analyzing mailer/subscribers.py
[00:05] Found 1 class with 5 public methods
[00:07] Phase 2: Gathering context from tests
[00:10] Extracted 8 usage patterns
[00:12] Phase 3: Generating API documentation
[00:20] Created docs/api/subscribers.md (1,234 words)
[00:22] Phase 4: Creating usage examples
[00:35] Created docs/examples/subscribers_usage.md (567 words)
[00:37] Phase 5: Validating documentation
[00:40] ✅ All checks passed
[00:42] Done! Documentation generated successfully.
```

## Summary

Documentation Generator Agent:
- ✅ Autonomous operation
- ✅ Comprehensive analysis
- ✅ Quality documentation output
- ✅ Validated and tested examples
- ✅ Consistent style
- ✅ Fast execution (30-60s)

**Invoke agent when you need documentation for any module in Mailer project.**
