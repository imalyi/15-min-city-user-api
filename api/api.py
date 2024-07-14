from fastapi import FastAPI
from api.categories.router import categories_router
from api.category_collections.router import (
    router as category_collections_router,
)
from api.addresses.router import router as addresses_router


app = FastAPI()

app.include_router(categories_router)
app.include_router(category_collections_router)
app.include_router(addresses_router)
