from collections.abc import AsyncIterator
from typing import Literal

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import ReferralCodes

from .base_dao import BaseDAO


class CodesDAO(BaseDAO):
    model = ReferralCodes

    @classmethod
    async def activate_deactivate(
        cls,
        state: Literal["activate", "deactivate"],
        session: AsyncIterator[AsyncSession],
        code_id: int,
    ) -> None:
        """"""
        if state == "activate":
            _bool = True
        elif state == "deactivate":
            _bool = False

        stmt = update(cls.model).where(cls.model.id == code_id).values(is_active=_bool)
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def deactivate_all(
        cls,
        session: AsyncIterator[AsyncSession],
        user_id: int,
    ) -> None:
        stmt = (
            update(cls.model)
            .where(cls.model.user_id == user_id)
            .values(is_active=False)
        )
        await session.execute(stmt)
        await session.flush()
