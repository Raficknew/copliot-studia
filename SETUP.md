# Mailer Setup Guide

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your SMTP credentials (optional for testing)
```

### 3. Run Tests
```bash
./test.sh
# or
pytest --cov=mailer
```

### 4. Run Application
```bash
./run.sh
# or
python -m mailer.web
```

Visit: http://localhost:5000

## Helper Scripts

### Run Application
```bash
./run.sh
```

### Run Tests with Coverage
```bash
./test.sh
```

### Lint Code
```bash
./lint.sh
```

### Format Code
```bash
./format.sh
```

## Development Workflow

1. Make code changes
2. Format code: `./format.sh`
3. Run tests: `./test.sh`
4. Check linting: `./lint.sh`
5. Commit changes

## Project Structure

```
copliot-studia/
├── mailer/                 # Main application package
│   ├── __init__.py
│   ├── web.py             # Flask application
│   ├── email_sender.py    # Email sending logic
│   ├── subscribers.py     # Subscriber management
│   └── validators.py      # Email validation
├── templates/             # HTML templates
│   └── index.html
├── static/               # Static assets
│   ├── style.css
│   └── script.js
├── tests/                # Test suite
│   ├── test_web.py
│   ├── test_email_sender.py
│   ├── test_subscribers.py
│   └── test_validators.py
├── .kiro/                # Kiro agent configurations
│   ├── agents/
│   └── skills/
├── requirements.txt      # Python dependencies
├── pytest.ini           # Pytest configuration
├── .pylintrc           # Pylint configuration
├── .env.example        # Environment variables template
├── run.sh              # Run application script
├── test.sh             # Run tests script
├── lint.sh             # Run linting script
└── format.sh           # Format code script
```

## Testing

The project has comprehensive test coverage (94%):
- 49 tests across 4 test files
- Email validation tests
- Subscriber management tests
- Email sending tests (with mocked SMTP)
- Flask web routes tests

## Code Quality

- **PEP 8 Compliance**: Enforced via pylint and black
- **Type Hints**: All functions have type annotations
- **Docstrings**: Google Docstring format
- **Test Coverage**: 94% overall
- **Linting Score**: 9.47/10

## Features

✅ Email validation (RFC 5322 compliant)
✅ Subscriber management (add/remove/list)
✅ Email sending with SMTP
✅ Web interface with Flask
✅ RESTful API endpoints
✅ Persistent storage (JSON)
✅ Comprehensive test suite
✅ Modern, responsive UI

## API Endpoints

- `GET /` - Main web interface
- `POST /api/subscribe` - Add subscriber
- `POST /api/unsubscribe` - Remove subscriber
- `GET /api/subscribers` - List all subscribers
- `POST /api/send-email` - Send email to all subscribers

## Environment Variables

Create a `.env` file (copy from `.env.example`):

```bash
FLASK_DEBUG=True
PORT=5000
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

**Note**: For Gmail, use an App Password instead of your regular password.
Generate one at: https://myaccount.google.com/apppasswords

## Troubleshooting

### Tests Failing
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Import Errors
```bash
# Make sure you're in the virtual environment
source venv/bin/activate
```

### SMTP Errors
- Check your SMTP credentials in `.env`
- For Gmail, enable "Less secure app access" or use App Passwords
- Check firewall settings

## Next Steps

1. ✅ Project structure created
2. ✅ All modules implemented
3. ✅ Tests passing (94% coverage)
4. ✅ Linting configured
5. ✅ Formatting configured
6. ✅ Helper scripts created
7. 🎯 Ready to use!

## Support

For issues or questions, refer to:
- README.md - Project overview
- requirements.md - Original requirements
- skills-agents-excersize.md - Exercise documentation
