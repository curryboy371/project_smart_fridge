from typing import List, Optional
from models.food_category import FoodCategoryModel
from core.tfdb import TFDB


class FoodCategoryCRUD:

    collection = TFDB.get_instance().food_category_collection 

    @classmethod
    async def create_category(cls, category: FoodCategoryModel) -> dict:
        category_dict = category.dict(by_alias=True)
        result = await cls.collection.insert_one(category_dict)
        created = await cls.collection.find_one({"_id": category_dict["_id"]})
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
        category = await cls.collection.find_one({"_id": category_id})
        return category

    @classmethod
    async def update_category(cls, category_id: str, category: FoodCategoryModel) -> Optional[dict]:
        category_dict = category.dict(by_alias=True)
        result = await cls.collection.update_one({"_id": category_id}, {"$set": category_dict})
        if result.matched_count == 0:
            return None
        updated = await cls.collection.find_one({"_id": category_id})
        return updated

    @classmethod
    async def delete_category(cls, category_id: str) -> bool:
        result = await cls.collection.delete_one({"_id": category_id})
        return result.deleted_count > 0