from api.dao.base import BaseDAO
from api.users.subscriptions.models import UserSubscription
from sqlalchemy import select, desc
from datetime import date
from api.database import async_session_maker


class UserSubscriptionDAO(BaseDAO):
    model = UserSubscription

    @classmethod
    async def activate_code(cls, code: str, user_id: int):
        pass

    
    @classmethod
    async def find_highest_active_subscription(cls, user_id: int):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .filter(
                    cls.model.user_id == user_id,
                    cls.model.date_to >= date.today()
                )
                .order_by(desc(cls.model.subscription_level))
            )

            result = await session.execute(query)
            return result.scalar() or None