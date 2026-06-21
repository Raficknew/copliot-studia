"""Flask web application for the Mailer service."""

import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from typing import Dict, Any
from .subscribers import SubscriberManager
from .email_sender import EmailSender
from .validators import EmailValidator

# Get the project root directory (parent of mailer package)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(project_root, 'templates')
static_dir = os.path.join(project_root, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
subscriber_manager = SubscriberManager()
email_sender = EmailSender()


@app.route("/")
def index() -> str:
    """Render main page with subscriber list.

    Returns:
        Rendered HTML template
    """
    subscribers = subscriber_manager.get_subscribers()
    count = subscriber_manager.get_subscriber_count()
    return render_template("index.html", subscribers=subscribers, count=count)


@app.route("/api/subscribe", methods=["POST"])
def subscribe() -> Dict[str, Any]:
    """Handle subscription request via API.

    Returns:
        JSON response with status and message

    Example Request:
        POST /api/subscribe
        {"email": "user@example.com"}

    Example Response:
        {"success": true, "message": "Subscribed successfully"}
    """
    try:
        data = request.get_json()
        
        if not data or "email" not in data:
            return jsonify({"success": False, "message": "Email is required"}), 400

        email = data["email"]

        # Validate email format
        if not EmailValidator.validate(email):
            return jsonify({"success": False, "message": "Invalid email format"}), 400

        # Add subscriber
        added = subscriber_manager.add_subscriber(email)
        
        if not added:
            return jsonify(
                {"success": False, "message": "Email already subscribed"}
            ), 400

        return jsonify({"success": True, "message": "Subscribed successfully"}), 201

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/unsubscribe", methods=["POST"])
def unsubscribe() -> Dict[str, Any]:
    """Handle unsubscribe request via API.

    Returns:
        JSON response with status and message
    """
    try:
        data = request.get_json()
        
        if not data or "email" not in data:
            return jsonify({"success": False, "message": "Email is required"}), 400

        email = data["email"]
        removed = subscriber_manager.remove_subscriber(email)

        if not removed:
            return jsonify(
                {"success": False, "message": "Email not found in subscriber list"}
            ), 404

        return jsonify({"success": True, "message": "Unsubscribed successfully"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/subscribers", methods=["GET"])
def get_subscribers() -> Dict[str, Any]:
    """Get list of all subscribers.

    Returns:
        JSON response with subscriber list and count
    """
    subscribers = subscriber_manager.get_subscribers()
    return jsonify(
        {"success": True, "subscribers": subscribers, "count": len(subscribers)}
    )


@app.route("/api/send-email", methods=["POST"])
def send_email() -> Dict[str, Any]:
    """Send email to all subscribers.

    Returns:
        JSON response with sending results

    Example Request:
        POST /api/send-email
        {"subject": "Newsletter", "body": "Hello subscribers!"}
    """
    try:
        data = request.get_json()

        if not data or "subject" not in data or "body" not in data:
            return jsonify(
                {"success": False, "message": "Subject and body are required"}
            ), 400

        subject = data["subject"]
        body = data["body"]
        html = data.get("html", False)

        subscribers = subscriber_manager.get_subscribers()

        if not subscribers:
            return jsonify(
                {"success": False, "message": "No subscribers to send email to"}
            ), 400

        results = email_sender.send_bulk(subscribers, subject, body, html=html)
        success_count = email_sender.get_success_count(results)

        return jsonify(
            {
                "success": True,
                "message": f"Sent to {success_count}/{len(subscribers)} subscribers",
                "sent": success_count,
                "total": len(subscribers),
            }
        ), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.errorhandler(404)
def not_found(error: Any) -> tuple:
    """Handle 404 errors.

    Args:
        error: Error object

    Returns:
        JSON response with error message
    """
    return jsonify({"success": False, "message": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error: Any) -> tuple:
    """Handle 500 errors.

    Args:
        error: Error object

    Returns:
        JSON response with error message
    """
    return jsonify({"success": False, "message": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
