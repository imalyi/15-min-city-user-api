from api.category_collections.models import CategoryCollections
from api.dao.base import BaseDAO
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from api.category_collections.models import CategoryCollections
from api.category_collections.categories.models import Categories
from api.database import async_session_maker
from sqlalchemy.orm import joinedload


class CategoryCollectionsDAO(BaseDAO):
    model = CategoryCollections

    @classmethod
    async def find_all(cls, is_hidden: bool = False, **filter_by):
        async with async_session_maker() as session:
            query = select(CategoryCollections).options(
                selectinload(
                    CategoryCollections.categories.and_(
                        Categories.is_hidden == is_hidden
                    )
                )
            )

            result = await session.execute(query)
            category_collections = result.scalars().all()

            # Sort CategoryCollections by their order field
            category_collections.sort(key=lambda collection: collection.order)

            # Sort Categories within each CategoryCollection by their order field
            for collection in category_collections:
                collection.categories = sorted(
                    (
                        category
                        for category in collection.categories
                        if category.is_hidden == is_hidden
                    ),
                    key=lambda category: category.order,
                )

            return category_collections
