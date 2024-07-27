from api.addresses.models import Address
from api.dao.base import BaseDAO
from api.database import async_session_maker
from sqlalchemy import select, insert
from fastapi_sa_orm_filter.main import FilterCore


def insert_percent_after_each_char(input_string):
    # Join each character in the input string with '%'
    return "%".join(input_string) + "%"


class AddressDAO(BaseDAO):
    model = Address
