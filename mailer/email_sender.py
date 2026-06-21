"""Email sending module with SMTP support."""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class EmailResult:
    """Result of email sending operation."""

    success: bool
    message: str
    failed_recipients: List[str]


class EmailSender:
    """Handles email sending operations."""

    def __init__(
        self,
        smtp_server: Optional[str] = None,
        smtp_port: Optional[int] = None,
        smtp_username: Optional[str] = None,
        smtp_password: Optional[str] = None,
        use_tls: bool = True,
    ):
        """Initialize email sender.

        Args:
            smtp_server: SMTP server address
            smtp_port: SMTP server port
            smtp_username: SMTP authentication username
            smtp_password: SMTP authentication password
            use_tls: Whether to use TLS encryption
        """
        self.smtp_server = smtp_server or os.getenv("SMTP_SERVER", "")
        self.smtp_port = smtp_port or int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = smtp_username or os.getenv("SMTP_USERNAME", "")
        self.smtp_password = smtp_password or os.getenv("SMTP_PASSWORD", "")
        self.use_tls = use_tls

    def send_email(
        self,
        recipients: List[str],
        subject: str,
        body: str,
        html: bool = False,
        sender: Optional[str] = None,
    ) -> EmailResult:
        """Send email to recipients.

        Args:
            recipients: List of recipient email addresses
            subject: Email subject
            body: Email body content
            html: Whether body is HTML format
            sender: Sender email address

        Returns:
            EmailResult with success status and details
        """
        if not recipients:
            return EmailResult(
                success=False,
                message="No recipients provided",
                failed_recipients=[],
            )

        if not self.smtp_server:
            return EmailResult(
                success=False,
                message="SMTP server not configured",
                failed_recipients=recipients,
            )

        sender_email = sender or self.smtp_username
        failed = []

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=30) as server:
                if self.use_tls:
                    server.starttls()

                if self.smtp_username and self.smtp_password:
                    server.login(self.smtp_username, self.smtp_password)

                for recipient in recipients:
                    try:
                        msg = self._create_message(
                            sender_email, recipient, subject, body, html
                        )
                        server.send_message(msg)
                    except Exception as e:
                        failed.append(recipient)
                        print(f"Failed to send to {recipient}: {e}")

            if failed:
                return EmailResult(
                    success=False,
                    message=f"Failed to send to {len(failed)} recipients",
                    failed_recipients=failed,
                )

            return EmailResult(
                success=True,
                message=f"Successfully sent to {len(recipients)} recipients",
                failed_recipients=[],
            )

        except Exception as e:
            return EmailResult(
                success=False,
                message=f"SMTP error: {str(e)}",
                failed_recipients=recipients,
            )

    def _create_message(
        self,
        sender: str,
        recipient: str,
        subject: str,
        body: str,
        html: bool,
    ) -> MIMEMultipart:
        """Create email message.

        Args:
            sender: Sender email address
            recipient: Recipient email address
            subject: Email subject
            body: Email body
            html: Whether body is HTML

        Returns:
            MIMEMultipart message object
        """
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipient

        mime_type = "html" if html else "plain"
        msg.attach(MIMEText(body, mime_type))

        return msg
