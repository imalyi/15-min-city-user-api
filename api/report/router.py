from fastapi import APIRouter
from api.users.user_manager import current_user_optional
from fastapi import Depends
from api.users.models import User
from fastapi import HTTPException
from api.subscriptions.models import SubscriptionLevel
from api.users.dao import UserDAO
from api.report.schemas import ReportCreate
from api.tasks.tasks import generate_report
from api.addresses.router import get_address_by_id
from api.category_collections.categories.router import get_category_by_id
from api.pois.models import POI
from sqlalchemy import select
from api.report.dao import ReportDAO

router = APIRouter(prefix="/report", tags=["Report"])


class UserSubscriptionLevelIsNotEnough(Exception):
    pass


class IncorrectCategoryID(Exception):
    pass


async def check_is_user_have_permissions_for_categories(
    user: User | None, report_request: ReportCreate
):
    for category_id in report_request.category_ids:
        category_level = await get_category_by_id(category_id)
        try:
            category_level = category_level.minimum_subscription_level
        except AttributeError:
            raise IncorrectCategoryID
        if category_level > user.subscription_level:
            raise UserSubscriptionLevelIsNotEnough
    return True


async def check_is_user_have_permission_for_custom_addresses(
    user: User | None, report_request: ReportCreate
):
    if user is None and report_request.custom_address_ids is not None:
        return False
    return True


async def check_user_permission_on_report(
    user: User | None, report_request: ReportCreate
):
    if not await check_is_user_have_permission_for_custom_addresses(
        user, report_request
    ):
        return False
    return True


@router.post("/")
async def generate_report_geojson(
    report_request: ReportCreate,
    user: User | None = Depends(current_user_optional),
):
    if not await check_user_permission_on_report(user, report_request):
        raise HTTPException(403, "User dont have permission")

    is_user_have_permission_for_categories = (
        await check_is_user_have_permissions_for_categories(
            user, report_request
        )
    )
    if not is_user_have_permission_for_categories:
        raise HTTPException(403, f"User dont have permission on category")

    nearest_pois = await ReportDAO.get_nearest_pois(report_request)
    nearest_pois_dict = await ReportDAO.create_dict(
        nearest_pois, report_request
    )
    generate_report.delay(nearest_pois_dict)
    return await ReportDAO.generate_geojson(nearest_pois_dict)
