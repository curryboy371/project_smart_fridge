from typing import List, Optional
from bson import ObjectId
from models.fridge_item import FridgeItemModel
from core.tfdb import TFDB
from core import tfenums as en

class FridgeItemCRUD:

    collection = TFDB.get_instance().get_collection(en.CollectionName.FRIDGE_ITEM)

    @classmethod
    async def create_item(cls, item: FridgeItemModel) -> dict:
        item_dict = item.dict(by_alias=True)
        item_dict.pop("_id", None)
        result = await cls.collection.insert_one(item_dict)
        created_item = await cls.collection.find_one({"_id": result.inserted_id})
        return created_item

    @classmethod
    async def get_items(cls) -> List[dict]:
        items = []
        cursor = cls.collection.find()
        async for item in cursor:
            items.append(item)
        return items

    @classmethod
    async def get_item(cls, item_id: str) -> Optional[dict]:
        if not ObjectId.is_valid(item_id):
            return None
        oid = ObjectId(item_id)
        item = await cls.collection.find_one({"_id": oid})
        return item
    

    @classmethod
    async def update_item(cls, item_id: str, item: FridgeItemModel) -> Optional[dict]:
        if not ObjectId.is_valid(item_id):
            return None
        item_dict = item.dict(by_alias=True)
        item_dict.pop("_id", None)
        oid = ObjectId(item_id)
        result = await cls.collection.update_one({"_id": oid}, {"$set": item_dict})
        if result.matched_count == 0:
            return None
        updated_item = await cls.collection.find_one({"_id": oid})
        return updated_item

    @classmethod
    async def delete_item(cls, item_id: str) -> bool:
        if not ObjectId.is_valid(item_id):
            return False
        
        oid = ObjectId(item_id)
        result = await cls.collection.delete_one({"_id": oid})
        return result.deleted_count > 0