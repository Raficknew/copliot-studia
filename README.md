# Mailer - Mailing List Management Application

A Python Flask application for managing mailing lists and sending emails to subscribers.

## Features

- ✉️ Subscriber management (add/remove subscribers)
- 📧 Email validation using RFC 5322 pattern
- 🚀 Bulk email sending to all subscribers
- 🌐 Web interface with Flask
- ✅ Comprehensive test suite with pytest
- 🎨 Modern, responsive UI

## Project Structure

```
mailer/
├── mailer/
│   ├── __init__.py
│   ├── email_sender.py      # Email sending logic
│   ├── subscribers.py       # Subscriber management
│   ├── validators.py        # Email validation
│   └── web.py              # Flask application
├── templates/              # HTML templates
│   └── index.html
├── static/                 # CSS and JavaScript
│   ├── style.css
│   └── script.js
├── tests/                  # Test suite
│   ├── test_email_sender.py
│   ├── test_subscribers.py
│   ├── test_validators.py
│   └── test_web.py
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md
```

## Setup

### 1. Create virtual environment

```bash
python3 -m venv venv
```

### 2. Activate virtual environment

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your SMTP credentials
```

## Running the Application

### Start the Flask server

```bash
python -m mailer.web
```

The application will be available at `http://localhost:5000`

## Running Tests

### Run all tests

```bash
pytest
```

### Run with coverage

```bash
pytest --cov=mailer --cov-report=html
```

### Run specific test file

```bash
pytest tests/test_subscribers.py
```

## API Endpoints

### Subscribe
```
POST /api/subscribe
Content-Type: application/json

{
  "email": "user@example.com"
}
```

### Unsubscribe
```
POST /api/unsubscribe
Content-Type: application/json

{
  "email": "user@example.com"
}
```

### Get Subscribers
```
GET /api/subscribers
```

### Send Email
```
POST /api/send-email
Content-Type: application/json

{
  "subject": "Newsletter",
  "body": "Hello subscribers!",
  "html": false
}
```

## Development

### Code Style

This project follows PEP 8 standards:
- Type hints for all functions
- Google Docstring format
- Maximum function length: 50 lines
- 80%+ test coverage

### Running Tests in Development

```bash
# Watch mode (re-run tests on file changes)
pytest-watch

# Run specific test
pytest tests/test_web.py::TestWebRoutes::test_subscribe_api_success
```

## Technologies

- **Python 3.9+**
- **Flask 3.0** - Web framework
- **pytest** - Testing framework
- **HTML/CSS/JavaScript** - Frontend

## License

MIT

## Author

Mailer Team
