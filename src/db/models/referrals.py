from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db import Base, int_pk


class Referrals(Base):
    __tablename__ = "referrals"

    id: Mapped[int_pk]
    referral_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    referrer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
