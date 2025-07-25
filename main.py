from typing import Union

from fastapi import FastAPI

from db import fetch_collection

app = FastAPI()

restaurants = fetch_collection()

# client = motor_asyncio.AsyncIOMotorClient()
# db = client.get_database("moodme")
# restaurants_collection = db.get_collection("restaurants")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None]=None):
    return {"Item Id": item_id, "Q": q}

@app.get("/restaurants")
async def fetch_restaurants():
    return await restaurants.find().to_list(5)