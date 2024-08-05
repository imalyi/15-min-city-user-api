from geoalchemy2.functions import ST_X, ST_Y, ST_Centroid, ST_Distance
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from api.addresses.models import Address
from api.category_collections.categories.models import Categories
from api.database import async_session_maker
from api.pois.models import POI
from api.report.schemas import ReportCreate


class ReportDAO:
    @classmethod
    async def get_nearest_pois(cls, report_request: ReportCreate):
        async with async_session_maker() as session:
            point_dict = await ReportDAO.get_centroid_by_address_id(
                report_request.address_id
            )
            point = await ReportDAO.create_WKE_point(point_dict)
            query = (
                select(
                    POI,
                    ST_X(ST_Centroid(Address.geometry)).label(
                        "center_longitude"
                    ),
                    ST_Y(ST_Centroid(Address.geometry)).label(
                        "center_latitude"
                    ),
                )
                .join(Address, POI.address_id == Address.id)
                .join(POI.categories)
                .where(Categories.id.in_(report_request.category_ids))
                .where(
                    ST_Distance(Address.geometry, point) * 111000
                    < report_request.distance
                )
                .options(joinedload(POI.address), joinedload(POI.categories))
            )

            result = await session.execute(query)

            pois = result.unique().all()
            return pois

    @classmethod
    async def create_dict(cls, pois, report_request: ReportCreate):
        data = {}
        data["start_point"] = {}
        data["start_point"].update(
            await ReportDAO.get_centroid_by_address_id(
                report_request.address_id
            )
        )
        data["pois"] = {}
        for poi, lon, lat in pois:
            for category in [category for category in poi.categories]:
                collection_title = category.collection.title
                category_titile = category.title
                if not data["pois"].get(collection_title):
                    data["pois"][collection_title] = {}
                if not data["pois"][collection_title].get(category_titile):
                    data["pois"][collection_title][category_titile] = []

                data["pois"][collection_title][category_titile].append(
                    {
                        "name": poi.name,
                        "location": {"lat": lat, "lon": lon},
                        "address": poi.address.to_dict(),
                    }
                )
        return data

    @classmethod
    async def get_centroid_by_address_id(cls, address_id: int):
        async with async_session_maker() as session:
            query = select(
                Address,
                ST_X(ST_Centroid(Address.geometry)).label("center_longitude"),
                ST_Y(ST_Centroid(Address.geometry)).label("center_latitude"),
            ).where(Address.id == address_id)
            result = await session.execute(query)
            result = result.first()
            return {
                "lat": result.center_latitude,
                "lon": result.center_longitude,
            }

    @classmethod
    async def create_WKE_point(cls, point):
        return func.ST_GeomFromText(
            f"POINT({point.get('lon')} {point.get('lat')})",
            4326,
        )
