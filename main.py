import logging
from fastapi import Depends, FastAPI
from database import MongoDatabase
import uvicorn

app = FastAPI()


def get_database():
    return MongoDatabase()


logging.basicConfig(level=logging.INFO)


@app.get("/address/from/name/{name}")
async def get_address_by_name(name: str, database: MongoDatabase = Depends(get_database)):
    results = database.search_by_partial_name(name)
    logging.info(results)
    return results


@app.get("/address/from/coordinates/{lon}/{lat}")
async def get_address_by_coordinates(lon: float, lat: float, database: MongoDatabase = Depends(get_database)):
    results = database.search_by_coordinates(lon, lat)
    logging.info(results)
    return results

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
