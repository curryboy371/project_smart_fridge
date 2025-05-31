
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
    

#temp
class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    username: str
    email: str
    age: Optional[int] = None

    class Config:
        arbitrary_types_allowed = True      # _id를 id로 자동 매핑
        json_encoders = {ObjectId: str}
        validate_by_name=True

        