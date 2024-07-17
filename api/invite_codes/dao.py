from api.dao.base import BaseDAO
from api.invite_codes.models import InviteCode


class InviteCodeDAO(BaseDAO):
    model = InviteCode
