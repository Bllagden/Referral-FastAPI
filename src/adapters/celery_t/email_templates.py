from email.message import EmailMessage

from pydantic import EmailStr

from settings import SMTPSettings, get_settings

_smtp_settings = get_settings(SMTPSettings)


def create_referral_registration_template(
    email_referral: EmailStr,
    email_to: EmailStr,
) -> EmailMessage:

    email = EmailMessage()
    email["Subject"] = "Referral-FastAPI"
    email["From"] = _smtp_settings.user
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>Новый реферал</h1>
            По вашему реферальному коду зарегистрировался новый пользователь - {email_referral}
        """,
        subtype="html",
    )
    return email
