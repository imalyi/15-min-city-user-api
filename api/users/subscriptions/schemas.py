from api.schemas.global_model import GlobalModelWithJSONAlias
from pydantic import Field
from datetime import date

class UserSubcription(GlobalModelWithJSONAlias):
    subscription_level: int
    date_from: date
    date_to: date
    is_active: bool
