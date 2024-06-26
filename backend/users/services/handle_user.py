import os

from django.core.mail import send_mail
from django.template.loader import render_to_string
from dotenv import load_dotenv

load_dotenv()


def handle_send_email_verify(email, code):
    context = {
        "code": code,
        "page": "email_confirmation"
    }

    send_mail(
        "Verify email",
        f"{code}",
        os.getenv('EMAIL_HOST_USER'),
        [email],
        fail_silently=False,
        # html_message=template
    )
