from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.engine.row import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import IncorrectEmailOrPasswordException
from settings import AuthSettings, get_settings

from ..dao import UsersDAO

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
_auth_settings = get_settings(AuthSettings)


def get_password_hash(password: str) -> str:
    return _pwd_context.hash(password)


def verify_password(plain_password: str, hashes_password: str) -> bool:
    return _pwd_context.verify(plain_password, hashes_password)


def create_access_token(user_id: str) -> str:  # ,data: dict
    """Создание JWT-токена. Истекает через 'access_token_expires'."""
    access_token_expires = timedelta(minutes=_auth_settings.access_token_expire_minutes)
    expire = datetime.now(tz=UTC) + access_token_expires

    to_encode = {"sub": user_id, "exp": expire}
    # {'sub': '1', 'exp': datetime(2023, 12, ...)}

    return jwt.encode(
        to_encode,
        _auth_settings.secret_key,
        _auth_settings.algorithm,
    )


async def authenticate_user(
    session: AsyncIterator[AsyncSession],
    email: str,
    password: str,
) -> RowMapping:
    user: RowMapping | None = await UsersDAO.find_one_or_none(session, email=email)
    if not user:
        raise IncorrectEmailOrPasswordException
    if not verify_password(password, user.hashed_password):
        raise IncorrectEmailOrPasswordException
    return user
