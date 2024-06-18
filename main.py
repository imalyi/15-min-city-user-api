import uvicorn
from fastapi import FastAPI

from report import router as report_router
from categories import router as categories_router
from address import router as address_router
from object import router as object_router
from user import router as user_router
from heatmap import router as heatmap_router

from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(middleware_class=CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

app.include_router(report_router, prefix='/report', tags=['Report'])
app.include_router(categories_router, prefix="/categories", tags=["Categories"])
app.include_router(address_router, prefix="/address", tags=["Address"])
app.include_router(object_router, prefix="/object", tags=["Objects"])
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(heatmap_router, prefix='/heatmap', tags=['Heat Map'])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
