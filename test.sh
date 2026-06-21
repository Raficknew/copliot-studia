#!/bin/bash
# Helper script to run tests

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Virtual environment not found. Please run setup first."
    exit 1
fi

# Run pytest with coverage
echo "Running tests with coverage..."
pytest --cov=mailer --cov-report=html --cov-report=term -v

echo ""
echo "Coverage report generated in htmlcov/index.html"
