from api.dao.base import BaseDAO
from api.users.subscriptions.models import UserSubscription


class SubscriptionDAO(BaseDAO):
    model = UserSubscription

    @classmethod
    async def activate_code(code: str, user_id: int):
        pass

    @classmethod
    async def get_user_subscriptions(user_id: int):
        pass
