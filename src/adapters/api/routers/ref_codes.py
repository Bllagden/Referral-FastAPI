from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError

from core.dao import CodesDAO
from core.ref_codes.codes import (
    create_expiry_date,
    generate_ref_code,
    valid_ref_code_data,
)
from core.ref_codes.schemas import (
    SRCode,
    SRCodeActivate,
    SRCodeCreate,
    SRCodeDeactivate,
)
from core.users.dependencies import get_current_user
from db import create_session
from db.models import Users
from exceptions import (
    RCodeAlreadyExistsException,
    RCodeDoesNotExistsException,
    RCodeGenLifetimeException,
)

# from dao import CodesDAO
# from ..users.dependencies import get_current_user
# from .codes import create_expiry_date, generate_ref_code, valid_ref_code_data
# from .schemas import SRCode, SRCodeActivate, SRCodeCreate, SRCodeDeactivate

router_ref_codes = APIRouter(prefix="/codes", tags=["Referral codes"])


@router_ref_codes.post("/add", response_model=SRCodeDeactivate)
async def add_ref_code(
    code_data: SRCodeCreate,
    current_user: Users = Depends(get_current_user),  # noqa: B008
) -> SRCodeDeactivate:
    """"""
    if not valid_ref_code_data(code_data.lifetime_days, code_data.lifetime_mins):
        raise RCodeGenLifetimeException

    ref_code = generate_ref_code()
    expiry_date = create_expiry_date(code_data.lifetime_days, code_data.lifetime_mins)

    async with create_session() as session:
        try:
            await CodesDAO.add(
                session,
                code=ref_code,
                user_id=current_user.id,
                expiry_date=expiry_date,
            )
        except IntegrityError as err:
            raise RCodeAlreadyExistsException from err

    return SRCodeDeactivate(
        code=ref_code,
        expiry_date=expiry_date,
    )


@router_ref_codes.delete("/delete", response_model=SRCode)
async def delete_ref_code(
    code: str,
    current_user: Users = Depends(get_current_user),  # noqa: B008
) -> SRCode:
    """"""
    async with create_session() as session:
        code_db = await CodesDAO.find_one_or_none(
            session,
            code=code,
            user_id=current_user.id,
        )
        if not code_db:
            raise RCodeDoesNotExistsException
        await CodesDAO.delete(session, id=code_db.id)
    return code_db


@router_ref_codes.patch("/activate", response_model=SRCodeActivate)
async def activate_ref_code(
    code: str,
    current_user: Users = Depends(get_current_user),  # noqa: B008
) -> SRCodeActivate:
    """"""
    async with create_session() as session:
        code_db = await CodesDAO.find_one_or_none(
            session,
            code=code,
            user_id=current_user.id,
        )
        if not code_db:
            raise RCodeDoesNotExistsException

        await CodesDAO.deactivate_all(session, current_user.id)
        await CodesDAO.activate_deactivate("activate", session, code_db.id)

    return SRCodeActivate(
        code=code_db.code,
        expiry_date=code_db.expiry_date,
    )


@router_ref_codes.patch("/deactivate", response_model=SRCodeDeactivate)
async def deactivate_ref_code(
    code: str,
    current_user: Users = Depends(get_current_user),  # noqa: B008
) -> SRCodeDeactivate:
    """"""
    async with create_session() as session:
        code_db = await CodesDAO.find_one_or_none(
            session,
            code=code,
            user_id=current_user.id,
        )
        if not code_db:
            raise RCodeDoesNotExistsException

        await CodesDAO.activate_deactivate("deactivate", session, code_db.id)

        return SRCodeDeactivate(
            code=code_db.code,
            expiry_date=code_db.expiry_date,
        )
