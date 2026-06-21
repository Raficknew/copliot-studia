"""Tests for email sending functionality."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from smtplib import SMTPException
from mailer.email_sender import EmailSender, EmailResult


class TestEmailSender:
    """Test suite for EmailSender class."""

    @pytest.fixture
    def mock_smtp(self) -> Mock:
        """Create mock SMTP client."""
        return Mock()

    @pytest.fixture
    def email_sender(self, mock_smtp: Mock) -> EmailSender:
        """Create EmailSender instance with mock SMTP."""
        return EmailSender(smtp_client=mock_smtp)

    def test_send_email_success(
        self, email_sender: EmailSender, mock_smtp: Mock
    ) -> None:
        """Test successful email sending."""
        result = email_sender.send("user@example.com", "Test Subject", "Test Body")
        
        assert result.success is True
        assert result.recipient == "user@example.com"
        assert result.error is None
        assert mock_smtp.sendmail.called

    def test_send_email_invalid_recipient(self, email_sender: EmailSender) -> None:
        """Test sending email with invalid recipient returns error."""
        result = email_sender.send("invalid@", "Subject", "Body")
        
        assert result.success is False
        assert result.recipient == "invalid@"
        assert result.error is not None

    def test_send_email_smtp_exception(
        self, email_sender: EmailSender, mock_smtp: Mock
    ) -> None:
        """Test sending email when SMTP raises exception."""
        mock_smtp.sendmail.side_effect = SMTPException("SMTP error")
        
        result = email_sender.send("user@example.com", "Subject", "Body")
        
        assert result.success is False
        assert "SMTP error" in result.error

    def test_send_email_with_html(
        self, email_sender: EmailSender, mock_smtp: Mock
    ) -> None:
        """Test sending HTML email."""
        html_body = "<h1>Test</h1>"
        result = email_sender.send(
            "user@example.com", "Subject", html_body, html=True
        )
        
        assert result.success is True
        assert mock_smtp.sendmail.called

    def test_send_email_with_custom_from(
        self, email_sender: EmailSender, mock_smtp: Mock
    ) -> None:
        """Test sending email with custom from address."""
        result = email_sender.send(
            "user@example.com",
            "Subject",
            "Body",
            from_email="custom@example.com",
        )
        
        assert result.success is True

    def test_send_bulk_emails(
        self, email_sender: EmailSender, mock_smtp: Mock
    ) -> None:
        """Test sending bulk emails to multiple recipients."""
        recipients = [
            "user1@example.com",
            "user2@example.com",
            "user3@example.com",
        ]
        
        results = email_sender.send_bulk(recipients, "Subject", "Body")
        
        assert len(results) == 3
        assert all(result.success for result in results)
        assert mock_smtp.sendmail.call_count == 3

    def test_send_bulk_with_invalid_email(
        self, email_sender: EmailSender, mock_smtp: Mock
    ) -> None:
        """Test bulk sending with one invalid email."""
        recipients = ["user1@example.com", "invalid@", "user2@example.com"]
        
        results = email_sender.send_bulk(recipients, "Subject", "Body")
        
        assert len(results) == 3
        assert results[0].success is True
        assert results[1].success is False
        assert results[2].success is True

    def test_get_success_count(self, email_sender: EmailSender) -> None:
        """Test counting successful email deliveries."""
        results = [
            EmailResult(success=True, recipient="user1@example.com"),
            EmailResult(success=False, recipient="user2@example.com", error="Error"),
            EmailResult(success=True, recipient="user3@example.com"),
        ]
        
        count = email_sender.get_success_count(results)
        assert count == 2

    def test_send_email_strips_whitespace(
        self, email_sender: EmailSender, mock_smtp: Mock
    ) -> None:
        """Test email validation strips whitespace from recipient."""
        result = email_sender.send("  user@example.com  ", "Subject", "Body")
        
        assert result.success is True
        assert result.recipient == "user@example.com"

    @patch.dict("os.environ", {"SMTP_HOST": "smtp.test.com", "SMTP_PORT": "587"})
    def test_initialization_from_environment(self) -> None:
        """Test EmailSender initialization uses environment variables."""
        sender = EmailSender()
        assert sender.smtp_host == "smtp.test.com"
        assert sender.smtp_port == 587

    def test_initialization_with_custom_settings(self) -> None:
        """Test EmailSender initialization with custom settings."""
        sender = EmailSender(
            smtp_host="custom.smtp.com",
            smtp_port=465,
            smtp_username="user",
            smtp_password="pass",
        )
        
        assert sender.smtp_host == "custom.smtp.com"
        assert sender.smtp_port == 465
        assert sender.smtp_username == "user"
        assert sender.smtp_password == "pass"
