from api.schemas.global_model import GlobalModelWithJSONAlias
from pydantic import Field
from datetime import date


class UserSubscriptionLimit(GlobalModelWithJSONAlias):
    report_requests: int = Field(ge=0)
    heatmap_requests: int = Field(ge=0)
    custom_address_check: int = Field(ge=0)


class UserSubcription(GlobalModelWithJSONAlias):
    subscription_level: int
    date_from: date
    date_to: date
    is_active: bool
