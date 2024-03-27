from collections.abc import AsyncIterator

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.models import Referrals, Users

from .base_dao import BaseDAO


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def get_active_code(
        cls,
        session: AsyncIterator[AsyncSession],
        email: str,
    ):
        """"""
        query = (
            select(cls.model)
            .filter_by(email=email)
            .options(selectinload(cls.model.referral_codes))
        )
        res = await session.execute(query)
        user = res.scalars().first()

        if user:
            for code in user.referral_codes:
                if code.is_active:
                    return code
        return None

    @classmethod
    async def get_cur_user(
        cls,
        session: AsyncIterator[AsyncSession],
        user_id: int,
    ):
        """"""
        query = (
            select(cls.model)
            .filter_by(id=user_id)
            .options(selectinload(cls.model.referral_codes))
        )
        res = await session.execute(query)

        user = res.scalars().first()
        user.referral_codes.sort(key=lambda code: code.expiry_date)
        return user

    @classmethod
    async def increment_referral_count(
        cls,
        session: AsyncIterator[AsyncSession],
        user_id: int,
    ) -> None:
        """"""
        stmt = (
            update(cls.model)
            .where(cls.model.id == user_id)
            .values(referral_count=cls.model.referral_count + 1)
        )
        await session.execute(stmt)

    @classmethod
    async def get_referrals_by_id(
        cls,
        session: AsyncIterator[AsyncSession],
        referrer_id: int,
    ):
        """"""
        query = (
            select(Users)
            .join(Referrals, Users.id == Referrals.referral_id)
            .filter(Referrals.referrer_id == referrer_id)
        )
        res = await session.execute(query)
        return res.scalars().all()
