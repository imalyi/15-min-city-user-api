from api.dao.base import BaseDAO
from api.pois.models import POI, POIAddresses, POICategories
from api.database import async_session_maker
from sqlalchemy import insert, select


class POIDAO(BaseDAO):
    model = POI

    @classmethod
    async def connect_to_address(cls, poi_id: int, address_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                stmt = insert(POIAddresses).values(
                    poi_id=poi_id, address_id=address_id
                )
                result = await session.execute(stmt)
                await session.commit()
        return result.scalar()

    @classmethod
    async def connect_to_category(cls, poi_id: int, category_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                stmt = insert(POICategories).values(
                    poi_id=poi_id, category_id=category_id
                )
                result = await session.execute(stmt)
                await session.commit()
        return result.scalar()

    @classmethod
    async def get_poi_categories(cls, poi_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                query = select(POICategories).where(poi_id=poi_id)
                return await session.execute(query).scalars().all()

    @classmethod
    async def get_poi_addresses(cls, poi_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                query = select(POIAddresses).where(poi_id=poi_id)
                return await session.execute(query).scalars().all()
