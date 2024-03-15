from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base, int_pk, str_255

if TYPE_CHECKING:
    from db.models import ReferralCodes


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    email: Mapped[str_255] = mapped_column(unique=True)
    hashed_password: Mapped[str_255]
    referral_count: Mapped[int] = mapped_column(default=0)

    referral_codes: Mapped[list["ReferralCodes"]] = relationship(
        "ReferralCodes",
        back_populates="referrer",
    )

    # rh_referrals: Mapped[list["Referrals"]] = relationship(
    #     "Referrals",
    #     back_populates="rh_referrer",
    # )

    # def __str__(self) -> str:
    #     return self.username
