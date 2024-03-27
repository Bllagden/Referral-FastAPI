import asyncio
from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_cache.decorator import cache
from sqlalchemy.exc import IntegrityError

from adapters.celery import send_referral_registration_to_referrer
from core.dao import CodesDAO, ReferralsDAO, UsersDAO
from core.ref_codes.schemas import SRCodeByEmail
from core.users.auth import authenticate_user, create_access_token, get_password_hash
from core.users.dependencies import get_current_user
from core.users.schemas import (
    SReferrals,
    SToken,
    SUserPresent,
    SUserRegister,
    SUserRegisterResponce,
)
from db import create_session
from db.models import Users
from exceptions import (
    RCodeDoesNotExistsException,
    ReferralsDoesNotExistsException,
    UserAlreadyExistsException,
)
from settings import AuthSettings, get_settings

router_users = APIRouter(prefix="/users", tags=["Users"])
router_users_auth = APIRouter(prefix="/users/auth", tags=["Auth & Users"])
_auth_settings = get_settings(AuthSettings)


@router_users.get("/referral_code_by_email", response_model=SRCodeByEmail)
@cache(expire=15)
async def get_code_by_email(email: str) -> SRCodeByEmail:
    """"""
    await asyncio.sleep(2)  # для демонстрации кеширования
    async with create_session() as session:
        code_db = await UsersDAO.get_active_code(session, email)
        if not code_db:
            raise RCodeDoesNotExistsException
        return SRCodeByEmail(
            code=code_db.code,
            expiry_date=code_db.expiry_date,
        )


@router_users.post("/register", response_model=SUserRegisterResponce)
async def register_user(user_data: SUserRegister) -> SUserRegisterResponce:
    hashed_password = get_password_hash(user_data.password)
    code_info = "Реферальный код не существует либо не активен"
    code = None

    async with create_session() as session:
        try:
            new_user = await UsersDAO.add(
                session,
                email=user_data.email,
                hashed_password=hashed_password,
            )
        except IntegrityError as err:
            raise UserAlreadyExistsException from err

        is_valid_ref_code = False
        if user_data.referrer_code:
            ref_code = await CodesDAO.find_one_or_none(
                session,
                code=user_data.referrer_code,
                is_active=True,
            )
            if (ref_code is not None) and ref_code.expiry_date > datetime.now(tz=UTC):
                is_valid_ref_code = True

        if is_valid_ref_code:
            referrer = await UsersDAO.find_one_or_none(
                session,
                id=ref_code.user_id,
            )
            await UsersDAO.increment_referral_count(
                session,
                referrer.id,  # ref_code.user_id
            )
            await ReferralsDAO.add(
                session,
                referral_id=new_user.id,
                referrer_id=referrer.id,  # ref_code.user_id
            )

            # celery
            send_referral_registration_to_referrer.delay(
                user_data.email,
                referrer.email,
            )

            code_info = "Реферальный код применен"
            code = ref_code.code
    return SUserRegisterResponce(status=200, code_info=code_info, code=code)


@router_users_auth.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> SToken:
    """"""
    async with create_session() as session:
        user = await authenticate_user(
            session,
            email=form_data.username,
            password=form_data.password,
        )
    access_token = create_access_token(str(user.id))
    return SToken(access_token=access_token, token_type=_auth_settings.token_type)


@router_users_auth.get("/me", response_model=SUserPresent)
async def get_cur_user(
    current_user: Users = Depends(get_current_user),  # noqa: B008
) -> SUserPresent:
    """"""
    async with create_session() as session:
        return await UsersDAO.get_cur_user(session, current_user.id)


@router_users_auth.get("/me/referrals", response_model=list[SReferrals])
@cache(expire=15)
async def get_referrals(
    current_user: Users = Depends(get_current_user),  # noqa: B008)
) -> list[SReferrals]:
    """"""
    await asyncio.sleep(2)  # для демонстрации кеширования
    async with create_session() as session:
        users_db = await UsersDAO.get_referrals_by_id(session, current_user.id)
        if not users_db:
            raise ReferralsDoesNotExistsException
            # return []
        return [
            SReferrals(
                id=user.id,
                email=user.email,
                referral_count=user.referral_count,
            )
            for user in users_db
        ]
