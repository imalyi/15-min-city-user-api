from api.schemas.global_model import GlobalModelWithJSONAlias
from pydantic import Field


class TicketCreate(GlobalModelWithJSONAlias):
    message: str = Field(min_length=5, max_length=10_000)
