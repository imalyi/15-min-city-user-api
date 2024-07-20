from api.schemas.global_model import GlobalModelWithJSONAlias
from pydantic import Field


class UserSubscriptionLimit(GlobalModelWithJSONAlias):
    report_requests: int = Field(ge=0)
    heatmap_requests: int = Field(ge=0)
    custom_address_check: int = Field(ge=0)
