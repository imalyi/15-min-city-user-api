from fastapi_users import schemas

from pydantic import Field


class UserRead(schemas.BaseUser[int]):
    subscription_level: int | None
    name: str


class UserCreate(schemas.BaseUserCreate):
    name: str


class UserUpdate(schemas.BaseUserUpdate):
    subscription_level: int | None
    name: str
