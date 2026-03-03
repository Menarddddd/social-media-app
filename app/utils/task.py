import aiosmtplib
from email.message import EmailMessage
from app.core.settings import settings

# TASKS LIVE HERE


async def send_email(receiver: str, subject: str, body: str):
    sender = settings.EMAIL_USER.get_secret_value()
    password = settings.EMAIL_PASS.get_secret_value()

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject

    msg.add_alternative(body, subtype="html")

    await aiosmtplib.send(
        msg,
        hostname="smtp.gmail.com",
        port=587,
        username=sender,
        password=password,
        start_tls=True,
    )
