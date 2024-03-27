import dotenv

dotenv.load_dotenv(".env.dev")

from .tasks import send_referral_registration_to_referrer  # noqa: E402

__all__ = [
    "send_referral_registration_to_referrer",
]
