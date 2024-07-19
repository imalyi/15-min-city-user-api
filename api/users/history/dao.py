from api.dao.base import BaseDAO
from api.users.history.models import UserHistory

from api.database import async_session_maker
from sqlalchemy import select, insert
from sqlalchemy import literal_column


class UserHistoryDAO(BaseDAO):
    model = UserHistory
