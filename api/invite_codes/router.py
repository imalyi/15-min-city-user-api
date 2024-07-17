from typing import List
from fastapi import APIRouter
from api.invite_codes.schemas import InviteCode, InviteCodeCreate
from api.invite_codes.dao import InviteCodeDAO
import random
import string
from api.users.user_manager import current_active_user, current_admin_user
from api.users.models import User
from fastapi import Depends

router = APIRouter(prefix="/invite-codes", tags=["Invite codes"])


def code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


@router.get("/", response_model=List[InviteCode])
async def get_all_invite_codes(user: User = Depends(current_admin_user)):
    return await InviteCodeDAO.find_all()


@router.post("/", response_model=InviteCode)
async def create_invite_code(
    new_invite_code_data: InviteCodeCreate,
    user: User = Depends(current_admin_user),
):
    code = code_generator()
    new_invite_code_data = new_invite_code_data.model_dump()
    new_invite_code_data["code"] = code
    result_id = await InviteCodeDAO.insert_data(new_invite_code_data)
    invite_code = await InviteCodeDAO.find_by_id(result_id)
    return invite_code
