from fastapi import APIRouter, Depends
from api.users.models import User
from api.users.user_manager import current_active_user
from api.users.limits.schemas import UserSubscriptionLimit
from api.users.history.dao import UserHistoryDAO

from api.subscriptions.router import get_all_subscription_levels
from api.users.subscriptions.router import get_user_subscription


router = APIRouter(prefix="/limits", tags=["Users requests count"])


@router.get("/")
async def get_user_limits(user: User = Depends(current_active_user)) -> UserSubscriptionLimit:
    used_requests_today = await UserHistoryDAO.get_used_requests_today(user.id)
    user_subscription_level = (await get_user_subscription(user)).subscription_level
    all_subscriptions = await get_all_subscription_levels()
    user_subscription = list(filter(lambda s: s.level == user_subscription_level, all_subscriptions))[0]
    allowed_requests_per_day = user_subscription.report_requests_per_day

    return UserSubscriptionLimit(used_report_requests=used_requests_today, allowed_requests_per_day=allowed_requests_per_day)
