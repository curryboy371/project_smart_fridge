from typing import Optional, List, Dict
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field
from models.model_base import PyObjectId

class FoodCategoryModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str
    storageMethod: str                        # 보관 방식 (예: "Refrigerated")
    shelfLifeDays: int                       # 보관 기간 (일수)
    allergenTags: Optional[List[str]] = None
    nutrition: Optional[List[str]] = None
    desc: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True      # _id를 id로 자동 매핑
        validate_by_name=True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}  # ObjectId 직렬화 대응