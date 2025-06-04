from crud.generic_crud import GenericCRUD
from core import tfenums as en
from datetime import datetime
from typing import List, Optional

import utils.validators
import utils.exceptions

class FridgeItemCRUD(GenericCRUD):
    def __init__(self, collection_enum: en.CollectionName):
        super().__init__(collection_enum)

    async def get_position_item(self, position) -> Optional[dict]:
        query = {"position": position.value if hasattr(position, "value") else position}
        return await self.collection.find_one(query)

    # 유통기한 지나지 않은 음식
    async def get_not_expired_items(self) -> List[dict]:
        results = []
        format = utils.validators.DATETIME_FORMAT_STRFTIME["hour"]
        now = datetime.now()
        cursor = self.collection.find({})
        async for doc in cursor:
            expire_str = doc.get("expire_dt")
            if expire_str:
                try:
                    expire_dt = datetime.strptime(expire_str, format)
                    if expire_dt >= now:
                        results.append(doc)
                except Exception as e:
                    utils.exceptions.raise_bad_request(detail=f"date parsing failed {e}")
        return results
         
        # str으로 변경된 것 처리    
        #cursor = self.collection.find({"expire_dt": {"$gte": now}})
        #return [doc async for doc in cursor]

    # 유통기한 지난 음식
    async def get_expired_items(self) -> List[dict]:
        results = []
        format = utils.validators.DATETIME_FORMAT_STRFTIME["hour"]
        now = datetime.now()
        cursor = self.collection.find({})
        async for doc in cursor:
            expire_str = doc.get("expire_dt")
            if expire_str:
                try:
                    expire_dt = datetime.strptime(expire_str, format)
                    if expire_dt < now:
                        results.append(doc)
                except Exception as e:
                    utils.exceptions.raise_bad_request(detail=f"date parsing failed {e}")
        return results
        #now = datetime.now()
        #cursor = self.collection.find({"expire_dt": {"$lt": now}})
        #return [doc async for doc in cursor]

    async def get_items_between_dates(self, start: datetime, end: datetime) -> List[dict]:
        
        format = utils.validators.DATETIME_FORMAT_STRFTIME["second"]  # "%Y-%m-%d %H:%M:%S"
        results = []
        cursor = self.collection.find({})  # 전부 불러온 뒤 필터링
        async for doc in cursor:
            expire_str = doc.get("expire_dt")
            if expire_str:
                try:
                    expire_dt = datetime.strptime(expire_str, format)
                    if start < expire_dt <= end:
                        results.append(doc)
                except Exception as e:
                    utils.exceptions.raise_bad_request(detail=f"date parsing failed {e}")
        return results
        
        #cursor = self.collection.find({
        #    "expire_dt": {
        #        "$gt": start,
        #        "$lte": end
        #    }
        #})
        #return [doc async for doc in cursor]