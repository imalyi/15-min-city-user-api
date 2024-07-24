from api.database import async_session_maker
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy import literal_column
from api.exceptions.unique import UniqueConstraintException


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            print(result)
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
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def insert_data(cls, data: dict):
        async with async_session_maker() as session:
            async with session.begin():
                stmt = (
                    insert(cls.model)
                    .values(**data)
                    .returning(literal_column("*"))
                )
                try:
                    result = await session.execute(stmt)
                    await session.commit()
                except IntegrityError:
                    raise UniqueConstraintException
        return result.scalar()
