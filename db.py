from motor import motor_asyncio

from typing import List, Optional

from bson import ObjectId

from pydantic import BaseModel, Field, GetJsonSchemaHandler
from pydantic_core.core_schema import ValidationInfo, no_info_wrap_validator_function, str_schema
from pydantic.json_schema import JsonSchemaValue

from datetime import datetime

class PyObjectId(ObjectId):

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        return no_info_wrap_validator_function(
            cls.validate,
            str_schema()
        )

    @classmethod
    def validate(cls, value: str, _info: ValidationInfo=None):
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid Object ID")
        return ObjectId(value)
    
    @classmethod
    def __get__pydantic__json_schema__(cls, _core_schema, handler: GetJsonSchemaHandler) -> JsonSchemaValue:
        return {"type": "string"}

class Address(BaseModel):
    building: str
    street: str

class Grade(BaseModel):
    date: datetime
    grade: str
    score: int

class Restaurant(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    address: Address
    cuisine: str
    grades: List[Grade]
    name: str = Field(...)
    restaurant_id: str = Field(...)

    class Config:
        allow_population_by_field_name: True
        arbitrary_types_allowed: True
        json_encoders = {
            ObjectId: str
        }

def fetch_collection():
    client = motor_asyncio.AsyncIOMotorClient()
    db = client.get_database("moodme")
    restaurants_collection = db.get_collection("restaurants")
    return restaurants_collection

async def fetch_documents(page_number, limit):
    restaurants = fetch_collection()
    cursor = restaurants.find({}).skip((page_number - 1) * limit).limit(limit)
    docs = []
    async for document in cursor:
        docs.append(Restaurant(**document))
    return docs