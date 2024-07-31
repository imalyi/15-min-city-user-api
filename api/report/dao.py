from api.dao.base import BaseDAO
from api.database import async_session_maker
from api.pois.categories.models import POICategories
from api.pois.models import POI
from sqlalchemy import select


class ReportDAO:

    @classmethod
    async def get_nearest_pois(cls, report_request):
        async with async_session_maker() as session:
            stmt = (
                select(POI)
                .join(POICategories, POI.id == POICategories.poi_id)
                .where(
                    POICategories.category_id.in_(report_request.category_ids)
                )
            )
            result = await session.execute(stmt)
            return result.scalars().all()
