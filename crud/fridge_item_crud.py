from typing import List, Optional
from bson import ObjectId
from models.fridge_item import FridgeItemModel
from core.tfdb import TFDB


class FridgeItemCRUD:

    collection = TFDB.get_instance().fridge_item_collection  # ⚠️ 컬렉션 이름 확인 필요

    @classmethod
    async def create_item(cls, item: FridgeItemModel) -> dict:
        item_dict = item.dict(by_alias=True)
        item_dict.pop("_id", None)
        result = await cls.collection.insert_one(item_dict)
        created_item = await cls.collection.find_one({"_id": result.inserted_id})
        return created_item

    @classmethod
    async def get_items(cls, user_id: str) -> List[dict]:
        if not ObjectId.is_valid(user_id):
            return []
        items = []
        cursor = cls.collection.find({"userId": ObjectId(user_id)})
        async for item in cursor:
            items.append(item)
        return items

    @classmethod
    async def get_item(cls, item_id: str) -> Optional[dict]:
        if not ObjectId.is_valid(item_id):
            return None
        item = await cls.collection.find_one({"_id": ObjectId(item_id)})
        return item

    @classmethod
    async def update_item(cls, item_id: str, item: FridgeItemModel) -> Optional[dict]:
        if not ObjectId.is_valid(item_id):
            return None
        item_dict = item.dict(by_alias=True)
        item_dict.pop("_id", None)
        result = await cls.collection.update_one({"_id": ObjectId(item_id)}, {"$set": item_dict})
        if result.matched_count == 0:
            return None
        updated_item = await cls.collection.find_one({"_id": ObjectId(item_id)})
        return updated_item

    @classmethod
    async def delete_item(cls, item_id: str) -> bool:
        if not ObjectId.is_valid(item_id):
            return False
        result = await cls.collection.delete_one({"_id": ObjectId(item_id)})
        return result.deleted_count > 0