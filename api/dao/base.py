from api.database import async_session_maker
from sqlalchemy import select, insert
from sqlalchemy import literal_column
from api.exceptions.unique import DBException
from asyncpg.exceptions import UniqueViolationError
from sqlalchemy.exc import IntegrityError


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
            return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.id == model_id)
            result = await session.execute(query)
            return result.unique().scalar_one_or_none()

    @classmethod
    async def insert_data(cls, data: dict):
        async with async_session_maker() as session:
            async with session.begin():
                stmt = (
                    insert(cls.model)
                    .values(**data)
                    .returning(literal_column("*"))
                )

                result = await session.execute(stmt)
                await session.commit()
                return result.fetchone()
