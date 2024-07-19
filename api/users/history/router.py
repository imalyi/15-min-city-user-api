from fastapi import APIRouter
from api.users.user_manager import current_active_user, current_admin_user
from api.users.models import User
from fastapi import Depends
from api.users.history.schemas import HistoryRecord
from api.users.history.dao import UserHistoryDAO

router = APIRouter(prefix="/history", tags=["User history"])


@router.get("/")
async def get_user_history(user: User = Depends(current_active_user)):
    return await UserHistoryDAO.find_all(user_id=user.id)


@router.get("/recent")
async def get_last_request(user: User = Depends(current_active_user)):
    pass


@router.get("/{history_record_id}")
async def get_record_by_id(
    history_record_id: int, user: User = Depends(current_active_user)
):
    pass


async def create_history_record(user: User, record: HistoryRecord):
    pass
