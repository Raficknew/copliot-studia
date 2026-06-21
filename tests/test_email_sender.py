"""Tests for email sending module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from mailer.email_sender import EmailSender, EmailResult


@pytest.fixture
def email_sender():
    """Create EmailSender instance for testing.

    Returns:
        EmailSender instance with test configuration
    """
    return EmailSender(
        smtp_server="smtp.test.com",
        smtp_port=587,
        smtp_username="test@test.com",
        smtp_password="password",
    )


class TestEmailSender:
    """Test cases for EmailSender class."""

    def test_send_email_no_recipients(self, email_sender: EmailSender):
        """Test sending email with no recipients."""
        result = email_sender.send_email([], "Subject", "Body")
        assert result.success is False
        assert "No recipients" in result.message

    def test_send_email_no_smtp_config(self):
        """Test sending email without SMTP configuration."""
        sender = EmailSender(smtp_server="")
        result = sender.send_email(["user@example.com"], "Subject", "Body")
        assert result.success is False
        assert "not configured" in result.message

    @patch("mailer.email_sender.smtplib.SMTP")
    def test_send_email_success(self, mock_smtp: Mock, email_sender: EmailSender):
        """Test successful email sending.

        Args:
            mock_smtp: Mocked SMTP class
            email_sender: EmailSender instance
        """
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        result = email_sender.send_email(
            ["user@example.com"], "Test Subject", "Test Body"
        )

        assert result.success is True
        assert "Successfully sent" in result.message
        assert len(result.failed_recipients) == 0
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once()

    @patch("mailer.email_sender.smtplib.SMTP")
    def test_send_email_multiple_recipients(
        self, mock_smtp: Mock, email_sender: EmailSender
    ):
        """Test sending email to multiple recipients.

        Args:
            mock_smtp: Mocked SMTP class
            email_sender: EmailSender instance
        """
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        recipients = ["user1@example.com", "user2@example.com"]
        result = email_sender.send_email(recipients, "Subject", "Body")

        assert result.success is True
        assert mock_server.send_message.call_count == 2

    @patch("mailer.email_sender.smtplib.SMTP")
    def test_send_email_partial_failure(
        self, mock_smtp: Mock, email_sender: EmailSender
    ):
        """Test email sending with partial failures.

        Args:
            mock_smtp: Mocked SMTP class
            email_sender: EmailSender instance
        """
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        mock_server.send_message.side_effect = [
            None,
            Exception("Send failed"),
        ]

        recipients = ["user1@example.com", "user2@example.com"]
        result = email_sender.send_email(recipients, "Subject", "Body")

        assert result.success is False
        assert len(result.failed_recipients) == 1
        assert "user2@example.com" in result.failed_recipients

    @patch("mailer.email_sender.smtplib.SMTP")
    def test_send_email_html(self, mock_smtp: Mock, email_sender: EmailSender):
        """Test sending HTML email.

        Args:
            mock_smtp: Mocked SMTP class
            email_sender: EmailSender instance
        """
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        html_body = "<html><body><h1>Test</h1></body></html>"
        result = email_sender.send_email(
            ["user@example.com"], "Subject", html_body, html=True
        )

        assert result.success is True
        mock_server.send_message.assert_called_once()

    @patch("mailer.email_sender.smtplib.SMTP")
    def test_send_email_smtp_exception(
        self, mock_smtp: Mock, email_sender: EmailSender
    ):
        """Test handling SMTP connection exception.

        Args:
            mock_smtp: Mocked SMTP class
            email_sender: EmailSender instance
        """
        mock_smtp.side_effect = Exception("Connection failed")

        result = email_sender.send_email(["user@example.com"], "Subject", "Body")

        assert result.success is False
        assert "SMTP error" in result.message
        assert "user@example.com" in result.failed_recipients
