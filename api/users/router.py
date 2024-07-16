from fastapi import FastAPI, APIRouter
from fastapi_users import FastAPIUsers

from api.users.models import User
from api.users.user_manager import get_user_manager
from api.users.schemas import UserRead, UserUpdate, UserCreate
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)

SECRET = "SECRET"

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

user_router = fastapi_users.get_users_router(UserRead, UserUpdate)
register_user_router = fastapi_users.get_register_router(UserRead, UserCreate)
