#!/bin/bash
# Helper script to run linting

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Virtual environment not found. Please run setup first."
    exit 1
fi

# Run pylint on mailer and tests directories
echo "Running pylint on mailer package..."
pylint mailer/

echo ""
echo "Running pylint on tests..."
pylint tests/

echo ""
echo "Linting complete!"
