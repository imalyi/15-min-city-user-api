from typing import List

from fastapi import APIRouter, Depends

from api.subscriptions.dao import SubscriptionDAO
from api.subscriptions.schema import SubscriptionLevel, SubscriptionLevelCreate
from api.users.models import User
from api.users.user_manager import current_admin_user

router = APIRouter(prefix="/subscription_levels", tags=["Subscription levels"])


@router.get("/", response_model=List[SubscriptionLevel])
async def get_all_subscription_levels(
    user: User = Depends(current_admin_user),
):
    return await SubscriptionDAO.find_all()


@router.post("/", response_model=int)
async def create_subscription_level(
    new_subscription_level_data: SubscriptionLevelCreate,
    user: User = Depends(current_admin_user),
):
    return await SubscriptionDAO.insert_data()
