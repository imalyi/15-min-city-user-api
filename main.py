from fastapi import FastAPI
import uvicorn
from database import MongoDatabase
app = FastAPI()

DATABASE = MongoDatabase()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/address/from/name/{name}")
async def say_hello(name: str):
    return DATABASE.search(name)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
