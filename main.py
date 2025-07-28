from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import fetch_documents, Restaurant

origins = [
    "http://localhost:3000"
]

app = FastAPI(
    title="Restaurants API",
    summary="A simple API to fetch restaurant data from a MongoDB collection."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/restaurants", 
        response_model=List[Restaurant], 
        response_description="Fetch restaurant data")
async def fetch_restaurants(page_number: int = 1, limit: int = 10):
    return await fetch_documents(page_number, limit)