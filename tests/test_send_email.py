from email.message import EmailMessage

from security_papers.config import EmailConfig
from security_papers.emailer import send_email


class DummySMTP:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.started_tls = False
        self.logged_in = False
        self.sent = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def starttls(self):
        self.started_tls = True

    def login(self, user, password):
        self.logged_in = True

    def send_message(self, message):
        assert isinstance(message, EmailMessage)
        self.sent = True



def test_send_email(monkeypatch):
    dummy = DummySMTP("smtp.example.com", 587)

    def _smtp(host, port):
        assert host == "smtp.example.com"
        assert port == 587
        return dummy

    monkeypatch.setattr("smtplib.SMTP", _smtp)

    config = EmailConfig(
        smtp_host="smtp.example.com",
        smtp_port=587,
        smtp_user="user",
        smtp_password="pass",
        smtp_starttls=True,
        mail_from="from@example.com",
        mail_to="to@example.com",
        subject_prefix="Security Papers",
    )

    message = EmailMessage()
    send_email(config, message)

    assert dummy.started_tls is True
    assert dummy.logged_in is True
    assert dummy.sent is True
