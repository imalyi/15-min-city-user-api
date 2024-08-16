from typing import List
from fastapi import APIRouter, HTTPException
from api.invite_codes.schemas import InviteCode, InviteCodeCreate
from api.invite_codes.dao import InviteCodeDAO
import random
import string
from api.users.user_manager import current_active_user, current_admin_user
from api.users.models import User
from fastapi import Depends, HTTPException

router = APIRouter(prefix="/invite-codes", tags=["Invite codes"])


async def get_invite_code_by_code(
    code: str,
):
    return await InviteCodeDAO.find_one_or_none(code=code)


def code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


@router.get("/", response_model=InviteCode)
async def get_invite_code_by_id(
    code_id: int, user: User = Depends(current_admin_user)
):
    return await InviteCodeDAO.find_one_or_none(id=code_id)


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
    new_invite_code_data["created_by"] = user.id
    result_id = (await InviteCodeDAO.insert_data(new_invite_code_data)).id
    invite_code = await InviteCodeDAO.find_by_id(result_id)
    return invite_code
