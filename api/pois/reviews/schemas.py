from api.schemas.global_model import GlobalModelWithJSONAlias
from pydantic import Field
from datetime import datetime


class ReviewCreate(GlobalModelWithJSONAlias):
    rating: int = Field(ge=1, le=5)
    wroted_at: datetime
    text: str = Field(min_length=1, max_length=8000)
