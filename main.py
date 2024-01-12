import logging

import uvicorn
from fastapi import Depends
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from database import MongoDatabase


logging.basicConfig(level=logging.INFO)
app = FastAPI()


app.add_middleware(middleware_class=CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)


def get_database():
    return MongoDatabase()


@app.get("/address/")
async def get_address_by_name(name: str=None, lon: float=None, lat: float=None, database: MongoDatabase = Depends(get_database)):
    if name:
        results = database.search_by_partial_name(name)
    elif lat is not None and lon is not None:
        results = database.search_by_coordinates(lon, lat)
    else:
        return {"error": "Invalid parameters"}
    logging.info(results)
    return results


@app.get('/report/')
async def get_report(address_id: str, database: MongoDatabase = Depends(get_database)):
    return database.get_report_from_id(address_id)


@app.get("/categories/")
async def get_categories(database: MongoDatabase = Depends(get_database)):
    return database.get_all_categories()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
