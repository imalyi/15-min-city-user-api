from api.addresses.models import Address
from api.dao.base import BaseDAO
from api.database import async_session_maker
from sqlalchemy import select, insert

from geoalchemy2.functions import ST_Contains, ST_GeomFromWKB, ST_Distance
from shapely.geometry import Point
from geoalchemy2.shape import from_shape
from sqlalchemy.dialects import postgresql


class AddressDAO(BaseDAO):
    model = Address

    @classmethod
    async def find_by_point(cls, filter):
        async with async_session_maker() as session:
            point = Point(filter.lon, filter.lat)
            point_wkb = from_shape(point)
            query = select(Address).filter(
                ST_Contains(Address.geometry, ST_GeomFromWKB(point_wkb, 4326))
            )
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            if result:
                return result
            query = (
                select(Address)
                .order_by(
                    ST_Distance(
                        Address.geometry, ST_GeomFromWKB(point_wkb, 4326)
                    )
                )
                .limit(1)
            )
            result = await session.execute(query)
            return result.first()
