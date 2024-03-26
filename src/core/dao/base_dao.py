from collections.abc import AsyncIterator

from sqlalchemy import delete, insert, select
from sqlalchemy.engine.row import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none(
        cls,
        session: AsyncIterator[AsyncSession],
        **filter_by,  # noqa: ANN003
    ) -> RowMapping | None:
        """"""
        query = select(cls.model.__table__.columns).filter_by(**filter_by)
        res = await session.execute(query)
        return res.mappings().one_or_none()

    @classmethod
    async def find_all(
        cls,
        session: AsyncIterator[AsyncSession],
        **filter_by,  # noqa: ANN003
    ) -> list[RowMapping]:
        """"""
        query = select(cls.model.__table__.columns).filter_by(**filter_by)
        res = await session.execute(query)
        return res.mappings().all()

    @classmethod
    async def add(
        cls,
        session: AsyncIterator[AsyncSession],
        **data,  # noqa: ANN003
    ):
        """"""
        stmt = insert(cls.model).values(**data).returning(cls.model)
        new_object = await session.execute(stmt)  # noqa: F841
        await session.flush()
        return new_object.scalar_one()

    @classmethod
    async def delete(
        cls,
        session: AsyncIterator[AsyncSession],
        **filter_by,  # noqa: ANN003
    ) -> None:
        """"""
        stmt = delete(cls.model).filter_by(**filter_by)
        await session.execute(stmt)
        await session.commit()
