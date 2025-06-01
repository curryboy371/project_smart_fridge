
from typing import Optional, List, Dict
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info):  # info 인자 추가
        if isinstance(v, ObjectId):
            return v
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema):
        if isinstance(core_schema, dict):
            core_schema.update(type="string")
            return core_schema
        return core_schema



class SimpleModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str
    value: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        validate_by_name = True
