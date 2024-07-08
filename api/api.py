"""
Fast API application
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.routers import category
from api.database import database
from api.routers import poi
from api.routers import address
from api.routers import user


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Lifespan of the application

    This async context manager is used to connect and disconnect from the database
    when the application starts and stops.
    """
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(
    category.prefrences_router,
    prefix="/preferences",
    tags=["Preferences"],
)
app.include_router(
    category.categories_router,
    prefix="/categories",
    tags=["Categories"],
)
app.include_router(address.router, prefix="/addresses", tags=["Addresses"])
app.include_router(poi.router, prefix="/pois", tags=["Points of interest"])
app.include_router(user.router, prefix="/users", tags=["User"])
