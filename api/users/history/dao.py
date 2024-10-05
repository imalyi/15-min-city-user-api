from api.dao.base import BaseDAO
from api.users.history.models import UserHistory

from api.database import async_session_maker
from sqlalchemy import select, insert
from sqlalchemy import literal_column

from sqlalchemy import select, func, text
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime, date

class UserHistoryDAO(BaseDAO):
    model = UserHistory



    @classmethod
    async def get_used_requests_today(cls, user_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                # Query for counting rows with today's date and unique start_point address
                stmt = select(func.count(UserHistory.id)).where(
                    UserHistory.user_id == user_id,
                    func.date(UserHistory.created_at) == date.today(),
                    UserHistory.request['start_point']['address'].isnot(None)  # Ensure address exists
                ).group_by(UserHistory.request['start_point']['full_address'])
                
                result = await session.execute(stmt)
                return result.scalar() or 0