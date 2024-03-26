import uuid
from datetime import UTC, datetime, timedelta


def valid_ref_code_data(lifetime_days: int, lifetime_mins: int) -> bool:
    if (lifetime_days <= 0 and lifetime_mins < 5) or lifetime_mins < 0:
        return False
    return True


def generate_ref_code() -> str:
    """b6bc9f2a-95a2-406c-8dc6-5b5a7791b8cb"""
    return str(uuid.uuid4())


def create_expiry_date(lifetime_days: int, lifetime_mins: int) -> datetime:
    return datetime.now(tz=UTC) + timedelta(
        days=lifetime_days,
        minutes=lifetime_mins,
    )
