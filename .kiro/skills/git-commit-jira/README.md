# Git Commit with Jira ID Skill

## Quick Start

This skill helps you create well-formatted git commits following the pattern:

```
JIRA-ID: One-line summary

Detailed description with:
- Specific changes made
- Context and reasoning
- Important notes
```

## Usage

When committing code, use this format to maintain consistent, professional commit messages that link to your Jira project management system.

### Quick Example
```bash
git commit -m "JIRA-1234: Add email validation" -m "
Detailed changes:
- Implemented RFC 5322 email validation
- Added comprehensive test coverage
- Updated documentation
"
```

## Files in This Skill

- **SKILL.md** - Complete documentation with examples, templates, and best practices
- **.promptyaml** - Configuration for when this skill activates
- **README.md** - This file (quick reference)

## Key Rules

1. ✅ Start with Jira ID (e.g., JIRA-1234, DEV-567)
2. ✅ Use imperative mood ("Add" not "Added")
3. ✅ Keep summary under 72 characters
4. ✅ Include blank line before detailed description
5. ✅ Explain WHY and WHAT in details

## Related Resources

- Full skill documentation: `SKILL.md`
- Git documentation: https://git-scm.com/docs
- Jira integration: https://confluence.atlassian.com/jirasoftwarecloud/referencing-issues-in-your-development-work-777002789.html
