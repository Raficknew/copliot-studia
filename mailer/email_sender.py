"""Email sending functionality for the Mailer application."""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from .validators import EmailValidator


@dataclass
class EmailResult:
    """Result of email sending operation.

    Attributes:
        success: Whether email was sent successfully
        recipient: Email address of recipient
        error: Error message if sending failed
    """

    success: bool
    recipient: str
    error: Optional[str] = None


class EmailSender:
    """Handles sending emails to subscribers."""

    def __init__(
        self,
        smtp_host: Optional[str] = None,
        smtp_port: Optional[int] = None,
        smtp_username: Optional[str] = None,
        smtp_password: Optional[str] = None,
        smtp_client: Optional[Any] = None,
    ) -> None:
        """Initialize email sender with SMTP configuration.

        Args:
            smtp_host: SMTP server hostname
            smtp_port: SMTP server port
            smtp_username: SMTP authentication username
            smtp_password: SMTP authentication password
            smtp_client: Mock SMTP client for testing
        """
        self.smtp_host = smtp_host or os.getenv("SMTP_HOST", "localhost")
        self.smtp_port = smtp_port or int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = smtp_username or os.getenv("SMTP_USERNAME", "")
        self.smtp_password = smtp_password or os.getenv("SMTP_PASSWORD", "")
        self._smtp_client = smtp_client

    def send(
        self,
        recipient: str,
        subject: str,
        body: str,
        from_email: Optional[str] = None,
        html: bool = False,
    ) -> EmailResult:
        """Send email to a single recipient.

        Args:
            recipient: Recipient email address
            subject: Email subject line
            body: Email body content
            from_email: Sender email address
            html: Whether body is HTML content

        Returns:
            EmailResult with success status and details

        Example:
            >>> sender = EmailSender()
            >>> result = sender.send("user@example.com", "Hello", "Test message")
            >>> result.success
            True
        """
        try:
            # Validate recipient email
            recipient = EmailValidator.validate_or_raise(recipient)

            # Create message
            msg = MIMEMultipart("alternative") if html else MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = from_email or self.smtp_username
            msg["To"] = recipient

            if html:
                msg.attach(MIMEText(body, "html"))

            # Send email
            if self._smtp_client:
                # Use mock client for testing
                self._smtp_client.sendmail(msg["From"], recipient, msg.as_string())
            else:
                # Use real SMTP connection
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    server.starttls()
                    if self.smtp_username and self.smtp_password:
                        server.login(self.smtp_username, self.smtp_password)
                    server.sendmail(msg["From"], recipient, msg.as_string())

            return EmailResult(success=True, recipient=recipient)

        except ValueError as e:
            return EmailResult(success=False, recipient=recipient, error=str(e))
        except smtplib.SMTPException as e:
            return EmailResult(
                success=False, recipient=recipient, error=f"SMTP error: {str(e)}"
            )
        except Exception as e:
            return EmailResult(
                success=False, recipient=recipient, error=f"Unexpected error: {str(e)}"
            )

    def send_bulk(
        self,
        recipients: List[str],
        subject: str,
        body: str,
        from_email: Optional[str] = None,
        html: bool = False,
    ) -> List[EmailResult]:
        """Send email to multiple recipients.

        Args:
            recipients: List of recipient email addresses
            subject: Email subject line
            body: Email body content
            from_email: Sender email address
            html: Whether body is HTML content

        Returns:
            List of EmailResult objects for each recipient
        """
        results = []
        for recipient in recipients:
            result = self.send(recipient, subject, body, from_email, html)
            results.append(result)
        return results

    def get_success_count(self, results: List[EmailResult]) -> int:
        """Count successful email deliveries.

        Args:
            results: List of EmailResult objects

        Returns:
            Number of successful deliveries
        """
        return sum(1 for result in results if result.success)
