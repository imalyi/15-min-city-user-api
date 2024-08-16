from api.dao.base import BaseDAO
from api.users.subscriptions.models import UserSubscription


class UserSubscriptionDAO(BaseDAO):
    model = UserSubscription

    @classmethod
    async def activate_code(cls, code: str, user_id: int):
        pass
