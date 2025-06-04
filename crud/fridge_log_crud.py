from crud.generic_crud import GenericCRUD
from core import tfenums as en
from datetime import datetime
from typing import List, Optional

class FridgeLogCRUD(GenericCRUD):
    def __init__(self, collection_enum: en.CollectionName):
        super().__init__(collection_enum)

    async def get_logs_by_event(self, event_type) -> List[dict]:
        query = {"event_type": event_type.value if hasattr(event_type, "value") else event_type}
        logs = []
        cursor = self.collection.find(query)
        async for log in cursor:
            logs.append(log)
        return logs
