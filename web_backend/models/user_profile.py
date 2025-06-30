from typing import Optional, List, Dict
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field
from models.model_base import TFBaseMdoel


class UserProfileModel(TFBaseMdoel):
    #id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    username: str
    age: Optional[int] = None
    gender: str
    allergies: Optional[List[str]] = None
    preferredCategories: Optional[List[str]] = None
    missingNutrients: Optional[List[str]] = None
    desc: Optional[str] = None
