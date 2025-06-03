from typing import Optional, List, Dict
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field
from models.model_base import TFBaseMdoel
from utils.validators import validate_datetime_string
from pydantic import validator
class FridgeLogModel(TFBaseMdoel):
    #id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id") 
    food_id: str                             # 음식 id
    name: str                                # 음식 이름 - food_category-name
    food_category: str                       # 음식 카테고리 - food category- category
    event_type:str                           # INBOUND | CONSUMED | DISCARDED    
    timestamp:str                            # 로그 발생 날짜
    entered_dt:str                           # 입고 날짜 
    expire_dt: Optional[str] = None          # 만료

    # @validator("entered_dt", "expire_dt", pre=True)
    # def validate_created_at_format(cls, v):
    #     if v:
    #         return validate_datetime_string(v, fmt="hour")
    #     return v