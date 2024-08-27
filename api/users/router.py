from api.users.schemas import UserRead, UserUpdate, UserCreate
from api.users.user_manager import fastapi_users, auth_backend

user_router = fastapi_users.get_users_router(UserRead, UserUpdate)
register_user_router = fastapi_users.get_register_router(UserRead, UserCreate)
auth_user_router = fastapi_users.get_auth_router(auth_backend)
verify_user_router = fastapi_users.get_verify_router(UserRead)
reset_user_password_router = fastapi_users.get_reset_password_router()
