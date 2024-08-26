from re import sub
from fastapi import APIRouter, HTTPException
from api.users.user_manager import current_active_user, current_admin_user
from fastapi import Depends
from api.contact.schemas import TicketCreate
from api.contact.dao import TicketDAO
from api.users.models import User
from api.services.send_email import send_simple_message
from api.exceptions import DuplicateEntryException

router = APIRouter(prefix="/contact", tags=["User tickets"])


async def notify_admins_about_new_ticket(data: dict):
    text = data.get("message")
    subject = f"New ticket"
    for admin_email in [
        "artsemstankevich@gmail.com",
        "tooawesomeforyou@mailbox.org",
        "monaslupska@gmail.com",
        "vkhram4enko@gmail.com",
    ]:
        send_simple_message(user_email=admin_email, subject=subject, text=text)


@router.post("/", status_code=202)
async def create_ticket(
    ticket: TicketCreate, user: User = Depends(current_active_user)
):
    data = ticket.model_dump()
    data["user_id"] = user.id
    try:
        result = await TicketDAO.insert_data(data)
        await notify_admins_about_new_ticket(data)
    except DuplicateEntryException:
        raise HTTPException(409, "Ticket already exists")
