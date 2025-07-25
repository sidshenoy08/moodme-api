from typing import List

from fastapi import FastAPI

from db import fetch_documents, Restaurant

app = FastAPI(
    title="Restaurants API",
    summary="A simple API to fetch restaurant data from a MongoDB collection."
)

@app.get("/restaurants", 
        response_model=List[Restaurant], 
        response_description="Fetch restaurant data")
async def fetch_restaurants(page_number: int = 1, limit: int = 10):
    return await fetch_documents(page_number, limit)