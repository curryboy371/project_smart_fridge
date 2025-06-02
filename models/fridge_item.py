from typing import Optional, List, Dict
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field
from models.model_base import TFBaseMdoel

#from models.model_base import PyObjectId


class FridgeItemModel(TFBaseMdoel):
    #id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id") 
    name: str                                # 음식 이름 - food_category-name
    food_category: Optional[str] = None      # 음식 카테고리 - food category - food category
    storageMethod: Optional[str] = None      # 보관 방식 (예: "Refrigerated")
    entered_dt: Optional[datetime] = None    # 냉장고에 들어온 날짜 및 시간
    expire_dt: Optional[datetime] = None     # 유통기한 또는 만료 날짜 (없다면 None)
    desc: Optional[str] = None               # 음식에 대한 추가 설명

    # class Config:
    #     arbitrary_types_allowed = True
    #     json_encoders = {
    #         ObjectId: str,
    #         datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
    #     }
    #     validate_by_name=True
