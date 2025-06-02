from typing import Optional, List, Dict
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field
from models.model_base import TFBaseMdoel

#from models.model_base import PyObjectId

class FridgeLogModel(TFBaseMdoel):
    #id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id") 
    food_id: str                             # 음식 id
    name: str                                # 음식 이름 - food_category-name
    food_category: str                       # 음식 카테고리 - food category- category
    event_type:str                           # INBOUND | CONSUMED | DISCARDED    
    timestamp:datetime                       # 로그 발생 날짜
    entered_dt:datetime                      # 입고 날짜 
    expire_dt: Optional[datetime] = None     # 만료

    # class Config:
    #     arbitrary_types_allowed = True
    #     json_encoders = {
    #         ObjectId: str,
    #         datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
    #     }
    #     validate_by_name=True
