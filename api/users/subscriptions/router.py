from fastapi import APIRouter
from api.users.user_manager import current_active_user, current_admin_user
from api.users.models import User
from fastapi import Depends
from api.users.subscriptions.schemas import UserSubscriptionLimit
from api.subscriptions.schema import SubscriptionLevel

router = APIRouter(prefix="/subscription", tags=["User subcription managment"])


@router.get("/limits", response_model=UserSubscriptionLimit)
async def get_user_limits(user: User = Depends(current_active_user)):
    pass


@router.post("/codes")
async def activate_code(code: str, user: User = Depends(current_active_user)):
    pass


@router.get("/", response_model=SubscriptionLevel)
async def get_user_subscription(user: User = Depends(current_active_user)):
    pass
