from typing import List, Optional
from models.food_category import FoodCategoryModel
from core.tfdb import TFDB
from bson import ObjectId
from core import tfenums as en

from core.tflog import TFLoggerManager as TFLog

class FoodCategoryCRUD():
    
    collection = TFDB.get_instance().get_collection(en.CollectionName.FOOD_CATEGORY)

    @classmethod
    async def create_category(cls, category: FoodCategoryModel) -> dict:
        category_dict = category.dict(by_alias=True)
        category_dict.pop("_id", None)  # _id 제거 (MongoDB가 자동 생성)
        result = await cls.collection.insert_one(category_dict)
        created = await cls.collection.find_one({"_id": result.inserted_id})
        return created

    @classmethod
    async def get_categories(cls) -> List[dict]:
        categories = []
        cursor = cls.collection.find()
        async for category in cursor:
            categories.append(category)
        return categories

    @classmethod
    async def get_category(cls, category_id: str) -> Optional[dict]:
        if not ObjectId.is_valid(category_id):
            return None
        oid = ObjectId(category_id)
        category = await cls.collection.find_one({"_id": oid})
        return category

    @classmethod
    async def update_category(cls, category_id: str, category: FoodCategoryModel) -> Optional[dict]:
        updated = await cls.collection.find_one({"category_id": category_id})
        # ID 유효성 검사
        if not ObjectId.is_valid(category_id):
            return None

        # Pydantic 모델을 dict로 변환하고 '_id' 필드 제거
        category_dict = category.dict(by_alias=True)
        category_dict.pop("_id", None)

        # 데이터 업데이트
        oid = ObjectId(category_id)
        result = await cls.collection.update_one(
            {"_id": oid},
            {"$set": category_dict}
        )

        # 수정된 문서 조회 후 반환
        updated = await cls.collection.find_one({"_id": oid})
        return updated
 
    @classmethod
    async def delete_category(cls, category_id: str) -> bool:
        if not ObjectId.is_valid(category_id):
            return None
        
        oid = ObjectId(category_id)
        result = await cls.collection.delete_one({"_id": oid})
        return result.deleted_count > 0
    
    @classmethod
    async def get_category_by_name(cls, name: str) -> Optional[dict]:
        category = await cls.collection.find_one({"name": name})
        return category
    