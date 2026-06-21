"""Main entry point for the Mailer application."""

from mailer.web import app

if __name__ == "__main__":
    print("🚀 Starting Mailer application...")
    print("📧 Access the application at: http://localhost:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)
