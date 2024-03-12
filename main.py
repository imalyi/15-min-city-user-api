import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from fastapi import Depends
from fastapi import APIRouter
from database.mongo_database import MongoDatabase
from database.get_database import get_database
from fastapi import FastAPI, HTTPException
from routers import report
from routers import categories
from routers import address
from mangum import Mangum

app = FastAPI()


APP_URL = 'https://api.cityinminutes.me/'


class ReportUrl:
    def __init__(self, address):
        self.address = address

    def __repr__(self):
        return f"{APP_URL}?report={self.address}&cat=joga"

    def __str__(self):
        return f"{APP_URL}?report={self.address}&cat=joga"


@app.get("/address")
async def get_address(name: str=None, database: MongoDatabase = Depends(get_database)):
    results = database.search_by_partial_name(name)
    results_with_url = []
    for result in results:
        results_with_url.append(str(ReportUrl(result)))
    if not results_with_url:
        raise HTTPException(status_code=404, detail="Address not found")
    return results_with_url


#app.include_router(report.router, prefix='/report', tags=['Report'])
#app.include_router(categories.router, prefix="/categories", tags=["Categories"])
#app.include_router(address.router, prefix="/address", tags=["Address"])


handler = Mangum(app)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
