from api.category_collections.models import CategoryCollections
from api.dao.base import BaseDAO
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from api.category_collections.models import CategoryCollections
from api.database import async_session_maker


class CategoryCollectionsDAO(BaseDAO):
    model = CategoryCollections

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(CategoryCollections).options(
                selectinload(CategoryCollections.categories)
            )
            result = await session.execute(query)
            return result.scalars().all()
