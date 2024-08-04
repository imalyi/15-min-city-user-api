from fastapi import APIRouter, Response
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
from celery.result import AsyncResult

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


@router.post("/", status_code=202, response_model=str)
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
    res = generate_report.delay(nearest_pois_dict)
    return res.id


@router.get("/{task_id}", status_code=200)
async def get_task_result(task_id: str):
    result = AsyncResult(task_id)

    if result.state == "PENDING":
        # Task hasn't been started yet
        return Response(
            {"task_id": task_id, "status": "Pending", "result": None},
            status_code=202,
        )
    elif result.state == "FAILURE":
        # Task failed
        return Response(
            {
                "task_id": task_id,
                "status": "Failed",
                "result": str(result.info),
            },
            status_code=500,
        )
    elif result.state == "SUCCESS":
        # Task succeeded
        return {
            "task_id": task_id,
            "status": "Success",
            "result": result.result,
        }
    else:
        # Task is still running
        return Response(
            {"task_id": task_id, "status": result.state, "result": None},
            status_code=202,
        )
