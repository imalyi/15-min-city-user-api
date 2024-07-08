from api.schemas.global_model import GlobalModelWithJSONAlias
from pydantic import Field, field_validator, ValidationError
from pydantic import EmailStr
from datetime import datetime


class UserCreate(GlobalModelWithJSONAlias):
    email: EmailStr
    password: str
    allow_telemetry: bool


class UserLogin(GlobalModelWithJSONAlias):
    email: EmailStr
    password: str


class User(GlobalModelWithJSONAlias):
    email: EmailStr
    registration_date: datetime


class UserSubscription(GlobalModelWithJSONAlias):
    id: int
    date_from: datetime
    date_to: datetime


class UserDailyRequestLimit(GlobalModelWithJSONAlias):
    daily_request_limit_report: int = Field(ge=0)
