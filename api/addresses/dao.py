from api.addresses.models import Address
from api.dao.base import BaseDAO
from api.database import async_session_maker
from sqlalchemy import select, insert

from geoalchemy2.functions import (
    ST_Contains,
    ST_GeomFromWKB,
    ST_Distance,
    ST_DistanceSphere,
)
from shapely.geometry import Point
from geoalchemy2.shape import from_shape
from sqlalchemy.dialects import postgresql


class AddressDAO(BaseDAO):
    model = Address

    @classmethod
    async def find_by_point(cls, filter):
        async with async_session_maker() as session:
            point = Point(filter.lon, filter.lat)
            point_wkb = from_shape(
                point, srid=4326
            )  # Ensure the SRID is set correctly

            # First, try to find an address containing the point
            query = select(Address).filter(
                ST_Contains(Address.geometry, ST_GeomFromWKB(point_wkb, 4326))
            )
            result = await session.execute(query)
            result = result.first()

            if result:
                return (
                    result,
                    0.0,
                )  # Distance is zero if the point is inside the geometry

            # If no containing geometry is found, find the closest one and calculate the distance in kilometers
            query = (
                select(
                    Address,
                    (
                        ST_DistanceSphere(
                            Address.geometry, ST_GeomFromWKB(point_wkb, 4326)
                        )
                    ).label("distance_m"),
                )
                .order_by(
                    ST_DistanceSphere(
                        Address.geometry, ST_GeomFromWKB(point_wkb, 4326)
                    )
                )
                .limit(1)
            )
            result = await session.execute(query)
            address, distance_m = result.unique().fetchone()
            return address, distance_m
