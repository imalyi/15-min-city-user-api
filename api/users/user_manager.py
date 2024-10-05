from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from sqlalchemy.sql.functions import user

from api.users.models import User, get_user_db
from fastapi_users import FastAPIUsers

from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)

from api.config import config
from api.services.send_email import send_simple_message
from api.users.subscriptions.free_trial import give_free_trial

def send_confifmation_email(user_email: str, token: str):
    send_simple_message(
        user_email=user_email,
        subject="Confirm Your email",
        text=f"https://cityinminutes.me/verify?token={token}",
    )


def send_password_recovery_email(user_email: str, token: str):
    send_simple_message(
        user_email=user_email,
        subject="Reset password",
        text=f"https://cityinminutes.me/reset_password?token={token}",
    )


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=config.JWT_SECRET, lifetime_seconds=3600)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)




bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(active=True, verified=True)
current_admin_user = fastapi_users.current_user(superuser=True)
current_user_optional = fastapi_users.current_user(optional=True)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = config.JWT_SECRET
    verification_token_secret = config.JWT_SECRET

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ):
        await give_free_trial(user.id)

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        send_password_recovery_email(user_email=user.email, token=token)

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        send_confifmation_email(user.email, token)
