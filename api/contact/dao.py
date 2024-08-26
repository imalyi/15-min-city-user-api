from api.dao.base import BaseDAO
from api.contact.models import Ticket


class TicketDAO(BaseDAO):
    model = Ticket
