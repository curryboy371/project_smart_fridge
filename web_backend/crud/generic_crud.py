from manager.tfdb_manager import TFDB
from core import tfenums as en
from bson import ObjectId
from typing import List, Optional, Any, Dict
from datetime import datetime, timedelta



class GenericCRUD:
    def __init__(self, collection_enum: en.CollectionName):
        self.collection = TFDB.get_instance().get_collection(collection_enum)

    async def create(self, data: dict) -> dict:
        data.pop("_id", None)  # MongoDB 자동 생성 ID 제거
        result = await self.collection.insert_one(data)
        created = await self.collection.find_one({"_id": result.inserted_id})
        return created

    async def get_all(self) -> List[dict]:
        items = []
        cursor = self.collection.find()
        async for data in cursor:
            items.append(data)
        return items
    
    async def get_by_name(self, name: str) -> Optional[dict]:
        data = await self.collection.find_one({"name": name})
        return data
    
    async def get_by_food_category_name(self, name: str) -> Optional[dict]:
        data = await self.collection.find_one({"food_category": name})
        return data


    async def get_by_id(self, item_id: str) -> Optional[dict]:
        if not ObjectId.is_valid(item_id):
            return None
        oid = ObjectId(item_id)
        data = await self.collection.find_one({"_id": oid})
        return data

    async def update(self, item_id: str, data: dict) -> Optional[dict]:
        if not ObjectId.is_valid(item_id):
            return None
        data.pop("_id", None)
        oid = ObjectId(item_id)
        await self.collection.update_one({"_id": oid}, {"$set": data})
        updated = await self.collection.find_one({"_id": oid})
        return updated

    async def delete(self, item_id: str) -> bool:
        if not ObjectId.is_valid(item_id):
            return False
        oid = ObjectId(item_id)
        result = await self.collection.delete_one({"_id": oid})
        return result.deleted_count > 0
