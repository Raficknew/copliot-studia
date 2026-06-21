#!/bin/bash
# Helper script to format code with black

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Virtual environment not found. Please run setup first."
    exit 1
fi

# Run black formatter
echo "Formatting code with black..."
black mailer/ tests/

echo ""
echo "Formatting complete!"
