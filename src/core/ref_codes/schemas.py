from datetime import datetime

from pydantic import BaseModel


class SRCodeByEmail(BaseModel):
    code: str
    expiry_date: datetime


class SRCode(SRCodeByEmail):
    is_active: bool


class SRCodeActivate(SRCode):
    is_active: bool = True


class SRCodeDeactivate(SRCode):
    is_active: bool = False


class SRCodeCreate(BaseModel):
    lifetime_days: int = 0
    lifetime_mins: int = 5
