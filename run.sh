#!/bin/bash
# Helper script to run the Mailer application

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Virtual environment not found. Please run setup first:"
    echo "python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Run the Flask application
echo "Starting Mailer application..."
python -m mailer.web
