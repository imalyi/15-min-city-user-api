from api.schemas.global_model import GlobalModelWithJSONAlias
from pydantic import Field
from typing import List


class Request(GlobalModelWithJSONAlias):
    category_ids: List[int]
    address_id: int
    custom_addresses: List[str]
    custom_pois: List[str]


class HistoryRecord(GlobalModelWithJSONAlias):
    id_: int = Field(alias="id")


class HistoryRecordCreate(HistoryRecord):
    user_id: int = Field(ge=0)
    request: Request
