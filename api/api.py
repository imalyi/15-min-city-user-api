from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.addresses.router import router as addresses_router
from api.category_collections.categories.router import categories_router
from api.category_collections.router import (
    router as category_collections_router,
)
from api.invite_codes.router import router as invite_codes_router
from api.pois.router import router as pois_router
from api.report.router import router as report_router
from api.subscriptions.router import router as subscription_router
from api.users.router import (
    auth_user_router,
    register_user_router,
    user_router,
)
from api.users.subscriptions.router import router as users_subscription_router

import sentry_sdk
from api.config import config

import logging


# DO NOT DELETE!
from api.tasks.celery import celery
import api.opensearch

# logging.disable(logging.WARNING)


sentry_sdk.init(
    dsn=config.SENTRY_DSN,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)


app = FastAPI()

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
app.include_router(users_subscription_router, prefix="/users")
app.include_router(report_router)
