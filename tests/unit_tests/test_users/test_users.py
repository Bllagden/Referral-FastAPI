from contextlib import nullcontext as does_not_raise

import pytest
from httpx import AsyncClient

from dao import UsersDAO
from db import create_session
from db.models import ReferralCodes
from exceptions import RCodeDoesNotExistsException

"""pytest --envfile .env.test tests/unit_tests/test_users -s -v"""


@pytest.mark.parametrize(
    "email, expectation",
    [
        ("1user@example.com", does_not_raise()),
        # ("2user@example.com", pytest.raises(RCodeDoesNotExistsException)),
        # ("3user@example.com", pytest.raises(RCodeDoesNotExistsException)),
    ],
)
async def test_rout_get_code_by_email(email: str, expectation, ac: AsyncClient):
    with expectation:
        response = await ac.get(f"/codes/get_code_by_email?email={email}")


@pytest.mark.parametrize(
    "email, expected_type",
    [
        ("1user@example.com", ReferralCodes),
        ("2user@example.com", type(None)),
        ("3user@example.com", type(None)),
    ],
)
async def test_dao_get_active_code_model(email: str, expected_type: type):
    async with create_session() as session:
        code = await UsersDAO.get_active_code(session, email)
        assert isinstance(code, expected_type)


@pytest.mark.parametrize(
    "email, expected_type",
    [
        ("1user@example.com", str),
        ("2user@example.com", type(None)),
        ("3user@example.com", type(None)),
    ],
)
async def test_dao_get_active_code_str(email: str, expected_type: type):
    async with create_session() as session:
        code = await UsersDAO.get_active_code(session, email)
        if code is not None:
            assert isinstance(code.code, expected_type)
        else:
            assert code is None
