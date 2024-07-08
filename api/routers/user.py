from fastapi import APIRouter, HTTPException
from typing import Optional

from api.database import user_table, subscription_level_table
from api.schemas.user import UserCreate
from api.database import user_table, database
from sqlalchemy import select
from api.schemas.user import User
from passlib.context import CryptContext
import datetime
from jose import jwt
from api.schemas.user import UserLogin

pwd_context = CryptContext(schemes=["bcrypt"])
JWT_ALGORITM = "HS256"
SECRET_KEY = "asfalsfMK"


credential_exception = HTTPException(
    status_code=401, detail="Could not validate credentials"
)


def access_tokex_expire_days():
    return 15


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_passsword: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_passsword, hashed_password)


def create_access_token(email: str):
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        days=access_tokex_expire_days()
    )
    jwt_data = {"sub": email, "exp": expire}
    encoded_jwt = jwt.encode(jwt_data, key=SECRET_KEY, algorithm=JWT_ALGORITM)
    return encoded_jwt


async def get_user_by_email(email: str):
    query = user_table.select().where(user_table.c.email == email)
    user = await database.fetch_one(query=query)
    return user


async def authenticate_user(email: str, password: str):
    user = await get_user_by_email(email)
    if not user:
        raise credential_exception
    if not verify_password(password, user.password):
        raise credential_exception
    return user


router = APIRouter()


@router.post("/", status_code=204)
async def create_user(user_data: UserCreate):
    data = user_data.model_dump()
    hashed_password = get_password_hash(data["password"])
    user = await get_user_by_email(data["email"])
    if user:
        raise HTTPException(409, "User exists")
    query = user_table.insert().values(
        email=data["email"], password=hashed_password
    )
    await database.execute(query=query)


@router.get("/", status_code=200, response_model=User, tags=["adminx"])
async def get_user(id: int):
    query = user_table.select().where(user_table.c.id == id)
    return await database.fetch_one(query=query)


@router.post("/token", status_code=200)
async def login_user(user: UserLogin):
    user = await authenticate_user(user.email, user.password)
    access_token = create_access_token(user.email)
    return {"access_token": access_token, "token_type": "bearer"}
