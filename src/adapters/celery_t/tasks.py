import smtplib

from pydantic import EmailStr

from settings import SMTPSettings, get_settings

from .email_templates import create_referral_registration_template
from .main import celery_app

_smtp_settings = get_settings(SMTPSettings)


@celery_app.task
def send_referral_registration_to_referrer(
    email_referral: EmailStr,
    email_to: EmailStr,
) -> None:
    """email_to - referrer email"""
    email_to = _smtp_settings.user  # отправка на свою почту
    msg_content = create_referral_registration_template(email_referral, email_to)

    with smtplib.SMTP_SSL(_smtp_settings.host, _smtp_settings.port) as server:
        server.login(_smtp_settings.user, _smtp_settings.password)
        server.send_message(msg_content)
