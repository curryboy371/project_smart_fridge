
from typing import Dict
from typing import Optional
from crud.generic_crud import GenericCRUD
from core import tfenums as en
from core.singlebone_base import TFSingletonBase
from datetime import datetime

class CrudManager(TFSingletonBase):
    """
    crud에 접근하여 db 조회를 하기 위한 crud 관리 manager
    api 단에서 다른 db에 조회할 때 사용함

    api를 생성하여 route를 include하는 시점에서 crud를 set 해줌
    """
    def __init__(self):
        if self._initialized:
            return
        super().__init__()
        self.cruds: Dict[en.CollectionName, GenericCRUD] = {}

    def set_crud(self, evalue : en.CollectionName, crud):
        self.cruds[evalue] = crud

    def get_crud(self, evalue: en.CollectionName) -> Optional[GenericCRUD]:
        return self.cruds.get(evalue)
    
    async def create_fridge_log_template(self, created: dict, event_type: en.EventType) -> dict:
        """
        냉장고 로그 생성용 템플릿 반환 함수
        """
        return {
            "name": created.get("name"),
            "food_id": str(created.get("_id")),
            "food_category": created.get("food_category"),
            "event_type": event_type.value,
            "timestamp": datetime.now(),
            "entered_dt": created.get("entered_dt"),
            "expire_dt": created.get("expire_dt")
        }
