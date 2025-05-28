from typing import Optional, List, Dict
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field

    
class FoodCategoryModel(BaseModel):
    id: str = Field(alias="_id")  # 문자열 ID 사용 (예: "egg", "milk")
    displayName: str
    recommendedShelfLifeDays: Dict[str, int]
    # 예: {"냉장": 7, "냉동": 30, "실온": 1}
    allergenTags: Optional[List[str]] = None
    nutrition: Optional[Dict[str, float]] = None
    # 예: {"calories": 120.5, "protein": 8.0}
    defaultExpireDays: Optional[int] = None

    class Config:
        validate_by_name=True