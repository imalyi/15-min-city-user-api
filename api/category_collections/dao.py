from api.category_collections.models import CategoryCollections
from api.dao.base import BaseDAO
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from api.category_collections.models import CategoryCollections
from api.categories.models import Categories
from api.database import async_session_maker


class CategoryCollectionsDAO(BaseDAO):
    model = CategoryCollections

    @classmethod
    async def find_all(cls, is_hidden: bool, **filter_by):
        async with async_session_maker() as session:
            query = select(CategoryCollections).options(
                selectinload(
                    CategoryCollections.categories.and_(
                        Categories.is_hidden == is_hidden
                    )
                )
            )

            result = await session.execute(query)
            return result.scalars().all()
