import os

from django.core.mail import send_mail
from django.template.loader import render_to_string
from dotenv import load_dotenv

load_dotenv()


def handle_send_email_verify(email: str, code: int) -> None:
    """
    Sends an email verification code to the specified email address.
    """
    context = {
        "code": code,
        "page": "email_confirmation"
    }

    template = render_to_string(
        "users/email_confirm.html", context)

    send_mail(
        "Verify email",
        f"{code}",
        os.getenv('EMAIL_HOST_USER'),
        [email],
        fail_silently=False,
        html_message=template
    )
