from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy import RowMapping

from db import create_session
from exceptions import (
    IncorrectTokenFormatException,
    TokenExpiredException,
    UserIsNotPresentException,
)
from settings import AuthSettings, get_settings

from ..dao import UsersDAO

_oauth2_schm = OAuth2PasswordBearer(tokenUrl="users/auth/token")
_auth_settings = get_settings(AuthSettings)


async def get_current_user(
    token: Annotated[str, Depends(_oauth2_schm)],
) -> RowMapping:
    """Получает JWT-токен. Декодирует токен в полезную нагрузку (dict) и проверяет ее.
    Далее, если в ней есть subject (id), ищет его в БД. Если такой есть, возвращает юзера.
    """
    try:
        payload = jwt.decode(token, _auth_settings.secret_key, _auth_settings.algorithm)
    except ExpiredSignatureError as err:
        raise TokenExpiredException from err
    except JWTError as err:
        raise IncorrectTokenFormatException from err

    user_id: str | None = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException

    async with create_session() as session:
        user = await UsersDAO.find_one_or_none(session, id=int(user_id))
        if not user:
            raise UserIsNotPresentException

        return user
