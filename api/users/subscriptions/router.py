from fastapi import APIRouter, HTTPException
from api.users.user_manager import current_active_user, current_admin_user
from api.users.models import User
from fastapi import Depends
from api.users.subscriptions.schemas import (
    UserSubscriptionLimit,
    UserSubcription,
)
from api.subscriptions.schema import SubscriptionLevel
from api.invite_codes.router import (
    get_invite_code_by_code,
)
from api.users.subscriptions.dao import UserSubscriptionDAO
from typing import Union
from api.users.subscriptions.models import (
    UserSubscription as UserSubcriptionModel,
)
from datetime import date, timedelta

router = APIRouter(prefix="/subscription", tags=["User subcription managment"])


@router.get("/limits", response_model=UserSubscriptionLimit)
async def get_user_limits(user: User = Depends(current_active_user)):
    pass


@router.post("/codes")
async def activate_code(code: str, user: User = Depends(current_active_user)):
    if not (await get_invite_code_by_code(code)):
        raise HTTPException(403, "Code not exists")
    new_subscription = await get_invite_code_by_code(code)
    if await get_user_subscription(user):
        raise HTTPException(409, "User already have active subscription")
    await UserSubscriptionDAO.insert_data(
        {
            "user_id": user.id,
            "subscription_level": new_subscription.level,
            "date_from": date.today(),
            "date_to": date.today() + timedelta(days=new_subscription.days),
        }
    )


@router.get("/", response_model=Union[UserSubcription, None])
async def get_user_subscription(user: User = Depends(current_active_user)):
    current_subscription = await UserSubscriptionDAO.find_one_or_none(
        order_by=UserSubcriptionModel.date_to.desc(), user_id=user.id
    )
    return current_subscription if current_subscription.is_active else None
