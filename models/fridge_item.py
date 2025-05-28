from typing import Optional, List, Dict
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field

from models.model_base import PyObjectId


class FridgeItemModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    userId: PyObjectId
    name: str
    categoryId: str  # 또는 PyObjectId로 변경 가능
    enteredAt: datetime
    lastUsedAt: Optional[datetime] = None
    usedCount: int = 0
    expireAt: Optional[datetime] = None
    memo: Optional[str] = None
    storageType: str  # 냉장 / 냉동 / 실온
    isUsedUp: bool = False

    usageHistory: Optional[List[Dict[str, Optional[str]]]] = None
    # usageHistory 예시: [{"usedAt": "2024-05-01", "note": "김치찌개로 사용"}]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        validate_by_name=True
