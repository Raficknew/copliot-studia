"""Flask web application for Mailer."""

import os
from typing import Dict, Any, Tuple
from flask import Flask, render_template, request, jsonify

from mailer.subscribers import SubscriberManager
from mailer.email_sender import EmailSender
from mailer.validators import EmailValidator


app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static",
)

# Initialize managers
subscriber_manager = SubscriberManager()
email_sender = EmailSender()


@app.route("/")
def index() -> str:
    """Render main page.

    Returns:
        Rendered HTML template
    """
    return render_template("index.html")


@app.route("/api/subscribe", methods=["POST"])
def subscribe() -> Tuple[Dict[str, Any], int]:
    """Add subscriber to mailing list.

    Returns:
        JSON response with status and HTTP status code
    """
    data = request.get_json()

    if not data or "email" not in data:
        return jsonify({"success": False, "error": "Email required"}), 400

    email = data["email"]

    if not EmailValidator.validate(email):
        return (
            jsonify({"success": False, "error": "Invalid email format"}),
            400,
        )

    try:
        added = subscriber_manager.add_subscriber(email)
        if added:
            return (
                jsonify(
                    {
                        "success": True,
                        "message": "Successfully subscribed",
                        "count": subscriber_manager.count(),
                    }
                ),
                201,
            )
        else:
            return (
                jsonify({"success": False, "error": "Already subscribed"}),
                409,
            )
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/unsubscribe", methods=["POST"])
def unsubscribe() -> Tuple[Dict[str, Any], int]:
    """Remove subscriber from mailing list.

    Returns:
        JSON response with status and HTTP status code
    """
    data = request.get_json()

    if not data or "email" not in data:
        return jsonify({"success": False, "error": "Email required"}), 400

    email = data["email"]
    removed = subscriber_manager.remove_subscriber(email)

    if removed:
        return (
            jsonify(
                {
                    "success": True,
                    "message": "Successfully unsubscribed",
                    "count": subscriber_manager.count(),
                }
            ),
            200,
        )
    else:
        return (
            jsonify({"success": False, "error": "Email not found"}),
            404,
        )


@app.route("/api/subscribers", methods=["GET"])
def get_subscribers() -> Tuple[Dict[str, Any], int]:
    """Get all subscribers.

    Returns:
        JSON response with subscribers list and HTTP status code
    """
    subscribers = subscriber_manager.get_subscribers()
    return (
        jsonify(
            {
                "success": True,
                "subscribers": subscribers,
                "count": len(subscribers),
            }
        ),
        200,
    )


@app.route("/api/send-email", methods=["POST"])
def send_email() -> Tuple[Dict[str, Any], int]:
    """Send email to all subscribers.

    Returns:
        JSON response with send result and HTTP status code
    """
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "error": "No data provided"}), 400

    subject = data.get("subject", "")
    body = data.get("body", "")
    html = data.get("html", False)

    if not subject or not body:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Subject and body required",
                }
            ),
            400,
        )

    subscribers = subscriber_manager.get_subscribers()

    if not subscribers:
        return (
            jsonify({"success": False, "error": "No subscribers"}),
            400,
        )

    result = email_sender.send_email(subscribers, subject, body, html)

    if result.success:
        return (
            jsonify(
                {
                    "success": True,
                    "message": result.message,
                    "sent_count": len(subscribers),
                }
            ),
            200,
        )
    else:
        return (
            jsonify(
                {
                    "success": False,
                    "error": result.message,
                    "failed": result.failed_recipients,
                }
            ),
            500,
        )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
