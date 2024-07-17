from fastapi import APIRouter
from api.users.user_manager import current_active_user, current_admin_user
from api.users.models import User
from fastapi import Depends

router = APIRouter("/subscription", tags=["User subcription managment"])


@router.get("/")
async def get_user_subscriptions(user: User = Depends(current_active_user)):
    pass


@router.post("/")
async def activate_code(code: str, user: User = Depends(current_active_user)):
    pass
