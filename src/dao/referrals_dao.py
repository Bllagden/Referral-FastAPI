from db.models import Referrals

from .base_dao import BaseDAO


class ReferralsDAO(BaseDAO):
    model = Referrals
