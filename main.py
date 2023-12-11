import logging
from fastapi import Depends, FastAPI
from database import MongoDatabase
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from typing import List

from fastapi import FastAPI, Query
app = FastAPI()


app.add_middleware(middleware_class=CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)


def get_database():
    return MongoDatabase()


logging.basicConfig(level=logging.INFO)


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
async def get_report(address_id: str, roles: List[int] = Query(None), database: MongoDatabase = Depends(get_database)):
    print(roles)
    return database.get_report_from_id(address_id)


@app.get('/roles')
async def get_roles():
    roles = [
        {'id': 1, 'title': 'Car Owner'},
        {'id': 2, 'title': 'Parent'},
        {'id': 3, 'title': 'Cyclist'},
        {'id': 4, 'title': 'Public Transport User'},
        {'id': 6, 'title': 'Pet Owner'},
        {'id': 7, 'title': 'Foodie'},
        {'id': 9, 'title': 'Book Lover'},
        {'id': 18, 'title': 'Sports Fan'},
        {'id': 20, 'title': 'Photographer'},
    ]
    return roles


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
