from api.schemas.global_model import GlobalModelWithJSONAlias
from pydantic import Field, computed_field


class SubscriptionLevelCreate(GlobalModelWithJSONAlias):
    title: str = Field(max_length=50)
    report_requests_per_day: int = Field(ge=0, default=0)
    heatmap_requests_per_day: int = Field(ge=0, default=0)
    custom_address_check_per_day: int = Field(ge=0, default=0)
    level: int = Field(ge=0)


class SubscriptionLevel(SubscriptionLevelCreate):
    id_: int = Field(alias="id")

    @computed_field
    @property
    def is_report_generating_allowed(self) -> bool:
        if self.report_requests_per_day == 0:
            return False
        return True

    @computed_field
    @property
    def is_heatmap_generation_allowed(self) -> bool:
        if self.heatmap_requests_per_day == 0:
            return False
        return True

    @computed_field
    @property
    def is_custom_address_check_allowed(self) -> bool:
        if self.custom_address_check_per_day == 0:
            return False
        return True
