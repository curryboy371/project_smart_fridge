from core.tfdb import TFDB
from core import tfenums as en
from bson import ObjectId
from typing import List, Optional

class GenericCRUD:
    def __init__(self, collection_enum: en.CollectionName):
        self.collection = TFDB.get_instance().get_collection(collection_enum)

    async def create(self, item: dict) -> dict:
        item.pop("_id", None)  # MongoDB 자동 생성 ID 제거
        result = await self.collection.insert_one(item)
        created = await self.collection.find_one({"_id": result.inserted_id})
        return created

    async def get_all(self) -> List[dict]:
        items = []
        cursor = self.collection.find()
        async for item in cursor:
            items.append(item)
        return items

    async def get_by_id(self, item_id: str) -> Optional[dict]:
        if not ObjectId.is_valid(item_id):
            return None
        oid = ObjectId(item_id)
        item = await self.collection.find_one({"_id": oid})
        return item

    async def update(self, item_id: str, item: dict) -> Optional[dict]:
        if not ObjectId.is_valid(item_id):
            return None
        item.pop("_id", None)
        oid = ObjectId(item_id)
        await self.collection.update_one({"_id": oid}, {"$set": item})
        updated = await self.collection.find_one({"_id": oid})
        return updated

    async def delete(self, item_id: str) -> bool:
        if not ObjectId.is_valid(item_id):
            return False
        oid = ObjectId(item_id)
        result = await self.collection.delete_one({"_id": oid})
        return result.deleted_count > 0
