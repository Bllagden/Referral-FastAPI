from pydantic import BaseModel, EmailStr

from ..ref_codes.schemas import SRCode


class SToken(BaseModel):
    access_token: str
    token_type: str


class SUserRegister(BaseModel):
    email: EmailStr
    password: str
    referrer_code: None | str = None


class SUserRegisterResponce(BaseModel):
    status: int
    code_info: str
    code: None | str = None


class SUserPresent(BaseModel):
    id: int
    email: str
    referral_count: int
    referral_codes: list[SRCode]


class SReferrals(BaseModel):
    id: int
    email: str
    referral_count: int
