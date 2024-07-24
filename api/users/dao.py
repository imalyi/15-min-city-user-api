from api.dao.base import BaseDAO
from api.users.models import User


class UserDAO(BaseDAO):
    model = User
