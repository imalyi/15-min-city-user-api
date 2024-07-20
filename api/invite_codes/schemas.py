from api.schemas.global_model import GlobalModelWithJSONAlias
from pydantic import Field


class InviteCodeCreate(GlobalModelWithJSONAlias):
    level: int = Field(ge=0)
    days: int = Field(ge=1, default=30)
    description: str
    created_by: int


class InviteCode(InviteCodeCreate):
    id_: int = Field(alias="id")
    code: str = Field(max_length=15, min_length=5)
    activated_by: int | None
