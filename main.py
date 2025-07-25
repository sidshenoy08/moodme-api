from typing import List

from fastapi import FastAPI

from db import fetch_documents, Restaurant

app = FastAPI()

@app.get("/restaurants", response_model=List[Restaurant])
async def fetch_restaurants(page_number: int = 1, limit: int = 10):
    return await fetch_documents(page_number, limit)