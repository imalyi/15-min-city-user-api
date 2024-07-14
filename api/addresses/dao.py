from api.addresses.models import Address
from api.dao.base import BaseDAO
from api.database import async_session_maker
from sqlalchemy import select, insert


def insert_percent_after_each_char(input_string):
    # Join each character in the input string with '%'
    return "%".join(input_string) + "%"


class AddressDAO(BaseDAO):
    model = Address

    @classmethod
    async def find_by_partial_name(cls, partial_name: str):
        async with async_session_maker() as session:
            query = select(cls.model).filter(
                Address.full_address.ilike(
                    insert_percent_after_each_char(partial_name)
                )
            )
            result = await session.execute(query)
            return result.scalars().all()
