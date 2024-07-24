from fastapi import APIRouter
from api.users.user_manager import current_user_optional
from fastapi import Depends
from api.users.models import User
from fastapi import HTTPException
from api.subscriptions.models import SubscriptionLevel
from api.users.dao import UserDAO
from api.report.schemas import ReportCreate

router = APIRouter(prefix="/report", tags=["Report"])


async def check_is_user_have_permissions_for_categories(
    user: User | None, report_request: ReportCreate
):
    pass


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
async def generate_router(
    report_request: ReportCreate,
    user: User | None = Depends(current_user_optional),
):
    if not await check_user_permission_on_report(user, report_request):
        raise HTTPException(403, "User dont have permission")
