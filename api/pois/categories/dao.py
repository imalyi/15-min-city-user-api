from api.dao.base import BaseDAO
from api.pois.categories.models import poi_category_association_table
from api.database import async_session_maker
from sqlalchemy import insert


class POICategoriesDAO(BaseDAO):
    model = poi_category_association_table

    @classmethod
    async def connect_to_category(cls, poi_id: int, category_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                stmt = insert(poi_category_association_table).values(
                    poi_id=poi_id, category_id=category_id
                )
                result = await session.execute(stmt)
                await session.commit()
        # return result.scalar()
