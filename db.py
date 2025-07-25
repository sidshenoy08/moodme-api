from motor import motor_asyncio


def fetch_collection():
    client = motor_asyncio.AsyncIOMotorClient()
    db = client.get_database("moodme")
    restaurants_collection = db.get_collection("restaurants")
    return restaurants_collection