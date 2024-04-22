import uvicorn
from fastapi import FastAPI

from routers import report
from routers import categories
from routers import address
from routers import object
from routers import user
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(middleware_class=CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

app.include_router(report.router, prefix='/report', tags=['Report'])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(address.router, prefix="/address", tags=["Address"])
app.include_router(object.router, prefix="/object", tags=["Objects"])
app.include_router(user.router, prefix="/user", tags=["User"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
