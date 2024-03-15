import asyncio
import json
from datetime import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy import insert

from app import create_app as create_fastapi_app
from db import Base, async_engine, async_session_factory
from db.models import ReferralCodes, Referrals, Users
from settings import DatabaseSettings, get_settings

"""pytest --envfile .env.test -s -v"""


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    assert get_settings(DatabaseSettings).mode == "TEST"

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    users = open_mock_json("users")
    referral_codes = open_mock_json("referral_codes")
    referrals = open_mock_json("referrals")

    # str -> datetime
    for code in referral_codes:
        code["expiry_date"] = datetime.strptime(
            code["expiry_date"], "%Y-%m-%d %H:%M:%S"
        )

    async with async_session_factory() as session:
        for Model, values in [
            (Users, users),
            (ReferralCodes, referral_codes),
            (Referrals, referrals),
        ]:
            stmt = insert(Model).values(values)
            await session.execute(stmt)

        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    """Async_Client.
    Клиент может быть использован для отправки HTTP-запросов к тестируемому веб-приложению
    """
    async with AsyncClient(app=create_fastapi_app(), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac():
    """HTTP-запросы к тестируемому веб-приложению с аутентификацией."""
    async with AsyncClient(app=create_fastapi_app(), base_url="http://test") as ac:
        await ac.post(
            "/users/auth/token",
            json={
                "username": "test@test.com",
                "password": "test",
            },
        )
        # assert ac.cookies["access_token"]
        yield ac
