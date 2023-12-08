import logging
from fastapi import Depends, FastAPI
from database import MongoDatabase
import uvicorn

app = FastAPI()


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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
