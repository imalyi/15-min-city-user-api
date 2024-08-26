from fastapi import APIRouter
from api.data_loaders.addresses.router import router as address_loader_router


router = APIRouter(prefix="/load", tags=["Load data"])
router.include_router(address_loader_router)
