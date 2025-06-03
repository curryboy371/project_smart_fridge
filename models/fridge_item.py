from typing import Optional, List, Dict
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, validator
from models.model_base import TFBaseMdoel
from core.tfenums import FridgePosition

from utils.validators import validate_datetime_string
from pydantic import validator

class FridgeItemModel(TFBaseMdoel):
    #id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id") 
    name: str                                   # 음식 이름 - food_category-name
    food_category: Optional[str] = None         # 음식 카테고리 - food category - food category
    storageMethod: Optional[str] = None         # 보관 방식 (예: "Refrigerated")
    entered_dt: Optional[str] = None            # 냉장고에 들어온 날짜 및 시간
    expire_dt: Optional[str] = None             # 유통기한 또는 만료 날짜 (없다면 None)
    position: Optional[int] = None              # 음식 위치
    desc: Optional[str] = None                  # 음식에 대한 추가 설명

    
    @validator("entered_dt", "expire_dt", pre=True)
    def validate_created_at_format(cls, v):
        if v:
            return validate_datetime_string(v, fmt="hour")  # 예: '2025-06-03 16
        return v