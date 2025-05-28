from typing import Optional, List, Dict
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field

from models.model_base import PyObjectId

class UserProfileModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    username: str
    age: Optional[int] = None
    sex: Optional[int] = None

    allergies: Optional[List[str]] = None
    preferredCategories: Optional[List[str]] = None
    notificationPreferences: Optional[Dict[str, Optional[str]]] = None
    # 예: {"notifyBeforeDays": 3, "channels": ["email", "sms"]}

    fridgeName: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        validate_by_name=True


