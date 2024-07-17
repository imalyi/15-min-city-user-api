from fastapi import FastAPI
from api.categories.router import categories_router
from api.category_collections.router import (
    router as category_collections_router,
)
from api.addresses.router import router as addresses_router
from api.pois.router import router as pois_router

from api.users.router import (
    user_router,
    register_user_router,
    auth_user_router,
)
from api.subscriptions.router import router as subscription_router

from api.invite_codes.router import router as invite_codes_router

app = FastAPI()

app.include_router(categories_router)
app.include_router(category_collections_router)
app.include_router(addresses_router)
app.include_router(pois_router)
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(
    register_user_router, prefix="/users", tags=["Register user"]
)
app.include_router(
    auth_user_router,
    prefix="/users",
    tags=["auth"],
)


app.include_router(subscription_router)
app.include_router(invite_codes_router)
