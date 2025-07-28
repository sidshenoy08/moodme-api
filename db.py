from motor import motor_asyncio

from typing import List, Optional

from bson import ObjectId

from pydantic import BaseModel, Field, GetJsonSchemaHandler
from pydantic_core.core_schema import ValidationInfo, no_info_wrap_validator_function, str_schema
from pydantic.json_schema import JsonSchemaValue

from datetime import datetime

from statistics import mode, StatisticsError

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

class Review(BaseModel):
    date: datetime
    grade: str
    score: int

class Restaurant(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    address: Address
    cuisine: str
    grades: List[Review]
    name: str = Field(...)
    restaurant_id: str = Field(...)
    full_address: Optional[str] = None
    avg_grade: Optional[str] = None

    class Config:
        allow_population_by_field_name: True
        arbitrary_types_allowed: True
        json_encoders = {
            ObjectId: str
        }

def compute_avggrade(reviews):
    grade_list = []
    for review in reviews:
        grade_list.append(review.grade)
    try:
        return mode(grade_list)
    except StatisticsError:
        return "N/A"

def fetch_collection():
    client = motor_asyncio.AsyncIOMotorClient()
    db = client.get_database("moodme")
    restaurants_collection = db.get_collection("restaurants")
    return restaurants_collection

async def fetch_grades():
    restaurants_collection = fetch_collection()
    distinct_grades = await restaurants_collection.distinct("grades.grade")
    return distinct_grades

async def fetch_documents(page_number, limit):
    restaurants_collection = fetch_collection()
    restaurant_docs = restaurants_collection.find({}).skip((page_number - 1) * limit).limit(limit)
    restaurants = []
    async for restaurant in restaurant_docs:
        curr_restaurant = Restaurant(**restaurant)
        curr_restaurant.full_address = curr_restaurant.address.building + " " + curr_restaurant.address.street
        curr_restaurant.avg_grade = compute_avggrade(curr_restaurant.grades)
        restaurants.append(curr_restaurant)
    return restaurants