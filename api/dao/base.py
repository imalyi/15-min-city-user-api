from sqlalchemy import literal_column, select, insert, update
from sqlalchemy.orm import query
from api.database import async_session_maker
from api.exceptions import DuplicateEntryException


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls, objects_filter=None):
        async with async_session_maker() as session:
            query = select(cls.model)
            if objects_filter:
                query = objects_filter.filter(query)
                query = objects_filter.sort(query)
            result = await session.execute(query)
            return result.scalars().unique().all()

    @classmethod
    async def find_one_or_none(cls, order_by=None, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)

            # Check if order_by is not None before applying it to the query
            if order_by is not None:
                query = query.order_by(order_by)

            result = await session.execute(query)
            return result.scalar() or None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.id == model_id)
            result = await session.execute(query)
            return result.unique().scalar_one_or_none()

    @classmethod
    async def insert_data(cls, data: dict):
        async with async_session_maker() as session:
            if await cls.find_one_or_none(order_by=None, **data):
                raise DuplicateEntryException("Row exist in db")
            async with session.begin():
                stmt = (
                    insert(cls.model)
                    .values(**data)
                    .returning(literal_column("*"))
                )

                result = await session.execute(stmt)
                await session.commit()
                return result.fetchone()[0]

    @classmethod
    async def update_data(cls, model_id: int, **update_data):
        async with async_session_maker() as session:
            async with session.begin():
                stmt = (
                    update(cls.model)
                    .where(cls.model.id == model_id)
                    .values(**update_data)
                    .returning(literal_column("*"))
                )
                result = await session.execute(stmt)
                await session.commit()
                row = result.fetchone()
                return row


