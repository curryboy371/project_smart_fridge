from crud.generic_crud import GenericCRUD
from core import tfenums as en
from datetime import datetime
from typing import List, Optional


class FridgeItemCRUD(GenericCRUD):
    def __init__(self, collection_enum: en.CollectionName):
        super().__init__(collection_enum)

    async def get_position_item(self, position) -> Optional[dict]:
        query = {"position": position.value if hasattr(position, "value") else position}
        return await self.collection.find_one(query)

    async def get_expired_items(self) -> List[dict]:
        now = datetime.now()
        cursor = self.collection.find({"expire_dt": {"$lt": now}})
        return [doc async for doc in cursor]

    async def get_items_between_dates(self, start: datetime, end: datetime) -> List[dict]:
        cursor = self.collection.find({
            "expire_dt": {
                "$gt": start,
                "$lte": end
            }
        })
        return [doc async for doc in cursor]