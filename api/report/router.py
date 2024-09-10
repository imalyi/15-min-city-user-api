from celery.result import AsyncResult
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from api.category_collections.categories.router import get_category_by_id
from api.report.dao import ReportDAO
from api.report.schemas import ReportCreate
from api.tasks.tasks import generate_report
from api.users.models import User
from api.users.user_manager import current_user_optional, current_active_user
from api.users.history.router import create_history_record
from api.exceptions import DuplicateEntryException, NotFoundException

router = APIRouter(prefix="/report", tags=["Report"])


class UserSubscriptionLevelIsNotEnough(Exception):
    pass


class IncorrectCategoryID(Exception):
    pass


async def check_is_user_have_permissions_for_categories(
    user: User, report_request: ReportCreate
):
    for category_id in report_request.category_ids:
        category_level = await get_category_by_id(category_id)
        if not category_level:
            raise NotFoundException
        try:
            category_level = category_level.minimum_subscription_level
        except AttributeError:
            raise IncorrectCategoryID
        if category_level > user.subscription_level:
            raise UserSubscriptionLevelIsNotEnough
    return True


async def check_is_user_have_permission_for_custom_addresses(
    user: User, report_request: ReportCreate
):
    if user is None and report_request.custom_address_ids is not None:
        return False
    return True


async def check_user_permission_on_report(
    user: User, report_request: ReportCreate
):
    if not await check_is_user_have_permission_for_custom_addresses(
        user, report_request
    ):
        return False
    return True


@router.post("/", status_code=202, response_model=str)
async def generate_report_geojson(
    report_request: ReportCreate,
    user: User = Depends(current_active_user),
):
    if not await check_user_permission_on_report(user, report_request):
        raise HTTPException(403, "User dont have permission")
    try:
        is_user_have_permission_for_categories = (
            await check_is_user_have_permissions_for_categories(
                user, report_request
            )
        )
    except NotFoundException:
        raise HTTPException(404, "Some categories not found")
    if not is_user_have_permission_for_categories:
        raise HTTPException(403, "User dont have permission on category")
    try:
        nearest_pois_dict = await ReportDAO.generate_report_create_for_celery(
            report_request
        )
    except NotFoundException:
        raise HTTPException(404, "Adress or category not found")
    try:
        await create_history_record(user, nearest_pois_dict)
    except DuplicateEntryException:
        pass

    res = generate_report.delay(nearest_pois_dict)
    return res.id


@router.get("/{task_id}", status_code=200)
async def get_task_result(
    task_id: str, request: Request, user: User = Depends(current_user_optional)
):
    result = AsyncResult(task_id)
    accept_header = request.headers.get("accept", "application/json")

    if result.state == "PENDING":
        response_data = {
            "task_id": task_id,
            "status": "Pending",
            "result": None,
        }
        return JSONResponse(content=response_data, status_code=202)
    elif result.state == "FAILURE":
        response_data = {
            "task_id": task_id,
            "status": "Failed",
            "result": str(result.info),
        }
        return JSONResponse(content=response_data, status_code=500)
    elif result.state == "SUCCESS":
        response_data = {
            "task_id": task_id,
            "status": "Success",
            "result": result.result,
        }

        if accept_header == "application/geojson":
            geojson_data = response_data.get("result", {}).get("geojson", {})
            return JSONResponse(content=geojson_data)
        elif accept_header == "application/json":
            json_ = response_data.get("result", {}).get("full", {})
            return JSONResponse(content=json_)
        elif accept_header == "application/json+geojson":
            return JSONResponse(content=response_data)
        else:
            raise HTTPException(422, "Header accept is not set")
    else:
        response_data = {
            "task_id": task_id,
            "status": result.state,
            "result": None,
        }
        return JSONResponse(content=response_data, status_code=202)
