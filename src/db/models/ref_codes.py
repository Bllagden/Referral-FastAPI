from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base, int_pk, str_255

if TYPE_CHECKING:
    from db.models import Users


class ReferralCodes(Base):
    __tablename__ = "referral_codes"

    id: Mapped[int_pk]
    code: Mapped[str_255] = mapped_column(unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    expiry_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)

    referrer: Mapped["Users"] = relationship(
        "Users",
        back_populates="referral_codes",
    )
