import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


from routers import report
from routers import categories
from routers import address
from mangum import Mangum


app = FastAPI()

app.include_router(report.router, prefix='/report', tags=['Report'])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(address.router, prefix="/address", tags=["Address"])

#app.add_middleware(middleware_class=CORSMiddleware,
#    allow_origins=['*'],
#    allow_credentials=True,
#    allow_methods=["*"],
#    allow_headers=["*"],)


handler = Mangum(app)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
