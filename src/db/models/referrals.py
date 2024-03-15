from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db import Base, int_pk


class Referrals(Base):
    __tablename__ = "referrals"

    id: Mapped[int_pk]
    referral_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    referrer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # referral_code_id: Mapped[int] = mapped_column(ForeignKey("referral_codes.id"))

    # rp_referral_code: Mapped["ReferralCodes"] = relationship(
    #     "ReferralCodes",
    #     back_populates="rp_referrals",
    # )
    # rp_referrer: Mapped["Users"] = relationship("Users", back_populates="rp_referrals")
