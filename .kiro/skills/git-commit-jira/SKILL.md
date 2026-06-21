# Git Commit with Jira ID Skill

## Purpose
This skill assists with creating well-formatted git commit messages that include a Jira ticket ID, a concise one-line description, and a detailed multi-line description of changes.

## Commit Message Format

### Standard Format
```
JIRA-1234: Brief one-line summary of changes

Detailed description of what was changed and why:
- Bullet point explaining specific change
- Another important modification
- Additional context or reasoning
- Any breaking changes or important notes
```

### Format Rules
1. **Jira ID**: Start with Jira ticket ID in format `PROJECT-NUMBER` (e.g., JIRA-1234, DEV-567, PROJ-890)
2. **Separator**: Use colon and space `: ` after Jira ID
3. **One-line Summary**: 
   - Maximum 72 characters (including Jira ID)
   - Use imperative mood ("Add feature" not "Added feature")
   - Don't end with period
   - Capitalize first word after colon
4. **Blank Line**: Always include blank line after one-line summary
5. **Detailed Description**:
   - Explain WHAT changed and WHY
   - Use bullet points for multiple changes
   - Wrap lines at 72 characters
   - Include context, reasoning, or important notes

## Examples

### Example 1: Feature Addition
```
JIRA-1234: Add email validation for subscriber registration

Detailed description of changes:
- Implemented RFC 5322 compliant email validation
- Added regex pattern to check email format
- Created EmailValidator class with static validate method
- Added comprehensive tests with parametrized test cases
- Prevents invalid email addresses from being stored
```

### Example 2: Bug Fix
```
DEV-567: Fix SMTP connection timeout in production

Fixed critical bug causing email sending failures:
- Increased SMTP connection timeout from 5s to 30s
- Added retry logic with exponential backoff
- Improved error handling and logging
- Updated environment variable SMTP_TIMEOUT documentation

This resolves production incidents where bulk emails
would fail due to slow network conditions.
```

### Example 3: Refactoring
```
PROJ-890: Refactor subscriber management into separate module

Reorganized code for better maintainability:
- Extracted subscriber logic from app.py to subscribers.py
- Created SubscriberManager class with clear responsibilities
- Added type hints to all public methods
- Improved docstrings following Google style
- Updated tests to reflect new module structure

No functional changes, purely structural improvements.
```

### Example 4: Documentation
```
DOC-445: Update README with installation instructions

Enhanced project documentation:
- Added step-by-step installation guide
- Included environment setup instructions
- Added troubleshooting section for common issues
- Updated dependencies list in README
- Added examples for running tests
```

### Example 5: Multiple Changes
```
JIRA-2001: Implement Flask API endpoints for subscribers

Added RESTful API for subscriber management:
- POST /api/subscribers - Add new subscriber with validation
- GET /api/subscribers - List all subscribers with pagination
- DELETE /api/subscribers/<id> - Remove subscriber by ID
- PUT /api/subscribers/<id> - Update subscriber information

Additional changes:
- Added JSON schema validation for API requests
- Implemented error responses with proper HTTP status codes
- Created API documentation in docs/api.md
- Added integration tests for all endpoints
- Updated requirements.txt with Flask-RESTful dependency
```

## Git Workflow Integration

### Command Pattern
```bash
# Stage changes
git add .

# Commit with formatted message
git commit -m "JIRA-1234: Brief summary" -m "
Detailed description:
- Change 1
- Change 2
- Change 3
"

# Or use git commit without -m to open editor
git commit
```

### Multi-line Commit in Terminal
```bash
git commit -m "JIRA-1234: Brief summary" \
-m "" \
-m "Detailed description:" \
-m "- Change 1" \
-m "- Change 2" \
-m "- Change 3"
```

### Using Commit Editor
For complex commits, use the editor:
```bash
git commit
```

Then write in the editor:
```
JIRA-1234: Brief one-line summary

Detailed description of changes:
- First important change
- Second important change
- Additional context

Technical details:
- Implementation approach
- Design decisions made
- Any trade-offs considered

Testing:
- Test coverage added
- Edge cases handled
```

## Commit Message Templates

### Template: New Feature
```
JIRA-XXXX: Add [feature name]

Implemented new feature for [purpose]:
- [Component/module created or modified]
- [Key functionality added]
- [Configuration or setup changes]
- [Tests added]

This feature enables [benefit/use case].
```

### Template: Bug Fix
```
JIRA-XXXX: Fix [brief issue description]

Resolved issue where [problem description]:
- [Root cause identified]
- [Solution implemented]
- [Additional safeguards added]

Fixes [specific symptom or error message].
```

### Template: Refactoring
```
JIRA-XXXX: Refactor [component name]

Improved code quality and maintainability:
- [Structural changes made]
- [Design patterns applied]
- [Dependencies cleaned up]

No functional changes, purely internal improvements.
```

### Template: Testing
```
JIRA-XXXX: Add tests for [component]

Increased test coverage for [module]:
- [Test scenarios added]
- [Edge cases covered]
- [Mocking strategy used]

Coverage improved from X% to Y%.
```

## Best Practices

### DO
✅ Use imperative mood in summary ("Add", "Fix", "Update", not "Added", "Fixed", "Updated")
✅ Include Jira ID at the start of every commit
✅ Keep summary line under 72 characters total
✅ Explain WHY changes were made, not just WHAT
✅ Use bullet points for clarity in detailed description
✅ Reference related issues or tickets
✅ Mention breaking changes prominently
✅ Include testing information when relevant

### DON'T
❌ Use past tense in summary ("Added feature" → "Add feature")
❌ End summary line with period
❌ Exceed 72 character line width
❌ Write vague descriptions ("Fix bug", "Update code")
❌ Commit without Jira ID
❌ Skip detailed description for non-trivial changes
❌ Include implementation details in summary line

## Validation Checklist

Before committing, verify:
- [ ] Jira ID is present and correct format
- [ ] Summary line is under 72 characters
- [ ] Summary uses imperative mood
- [ ] Blank line separates summary from details
- [ ] Detailed description explains WHY and WHAT
- [ ] Important changes are highlighted
- [ ] Breaking changes are clearly noted
- [ ] Related tickets/issues are referenced

## Integration with Git Hooks

### Pre-commit Hook Validation
You can create a commit-msg hook to validate format:
```bash
#!/bin/bash
# .git/hooks/commit-msg

commit_msg=$(cat "$1")

# Check for Jira ID format
if ! echo "$commit_msg" | grep -qE "^[A-Z]+-[0-9]+:"; then
    echo "❌ Commit message must start with Jira ID (e.g., JIRA-1234:)"
    exit 1
fi

# Check summary length (first line)
first_line=$(echo "$commit_msg" | head -n1)
if [ ${#first_line} -gt 72 ]; then
    echo "❌ Summary line exceeds 72 characters"
    exit 1
fi

echo "✅ Commit message format validated"
```

## Quick Reference Card

```
Format:  JIRA-####: Summary (imperative, <72 chars)
         [blank line]
         Detailed description:
         - Bullet points
         - Additional context
         
Example: JIRA-1234: Add user authentication

         Implemented JWT-based authentication:
         - Created auth middleware
         - Added login/logout endpoints
         - Integrated with user database
         
         This enables secure user sessions.
```

## Common Jira Prefixes

Adapt the Jira ID format to your organization:
- `JIRA-####` - Generic Jira ticket
- `DEV-####` - Development tasks
- `BUG-####` - Bug fixes
- `FEAT-####` - New features
- `DOC-####` - Documentation
- `TEST-####` - Testing improvements
- `REFACTOR-####` - Code refactoring
- `HOTFIX-####` - Emergency fixes

## Summary

This skill ensures consistent, informative commit messages that:
1. Link to project management (Jira)
2. Provide quick context (one-line summary)
3. Offer detailed explanation (description)
4. Follow industry best practices
5. Enable better collaboration and code review

Use this format for all commits to maintain a clean, professional git history that's easy to navigate and understand.
