from fastapi import APIRouter
from models.fridge_log import FridgeLogModel
from crud.generic_crud import GenericCRUD
from typing import List

from typing import Optional
from datetime import datetime, timedelta

from api.routes_exception import *
from core import tfenums as en
from core.tflog import TFLoggerManager as TFLog

from crud.crud_manager import CrudManager


class FridgeLogAPI():
    def __init__(self, enum_value: en.CollectionName):
        self._enum_value = enum_value
        self._log = TFLog.get_instance()
        self._crud = GenericCRUD(enum_value)  # GenericCRUD 사용, enum 값 넘겨서 초기화

        # API 경로 등록
        self._router = APIRouter(prefix=f"/{self._enum_value.value}")

        self._router.get("/", response_model=List[FridgeLogModel])(self.get_datas)
        self._router.get("/{item_id}", response_model=FridgeLogModel)(self.get_data)
        self._router.post("/", response_model=FridgeLogModel)(self.create_data)
        self._router.put("/", response_model=FridgeLogModel)(self.update_data)
        self._router.delete("/{item_id}")(self.delete_data)

    @property
    def router(self):
        return self._router
    
    @property
    def crud(self):
        return self._crud

    async def get_datas(self):
        return await self._crud.get_all()

    async def get_data(self, data_id: str):
        data = await self._crud.get_by_id(data_id)
        if not data:
            self._log.logger.warning(f"invalid log id({data_id})")
            raise_not_found(detail="Fridge log not found")
        return data

    async def create_data(self, data: FridgeLogModel):
        data_id = data.id
        self._log.logger.info(f"try create fridge log id({data_id})")

        if data.timestamp is None:
            data.timestamp = datetime.utcnow()

        created = await self._crud.create(data.dict(by_alias=True))
        if not created:
            self._log.logger.warning(f"failed create fridge log id({data_id})")
            raise_bad_request()

        self._log.logger.info(f"success create fridge log id({data_id})")
        return created

    async def update_data(self, data: FridgeLogModel):
        data_id = data.id
        self._log.logger.info(f"try update fridge log id({data_id})")

        updated = await self._crud.update(data_id, data.dict(by_alias=True))
        if not updated:
            self._log.logger.warning(f"failed update fridge log id({data_id})")
            raise_bad_request()

        self._log.logger.info(f"success update fridge log id({data_id})")
        return updated

    async def delete_data(self, data_id: str):
        self._log.logger.info(f"try delete fridge log id({data_id})")

        data = await self._crud.get_by_id(data_id)
        if not data:
            self._log.logger.warning(f"invalid fridge log id({data_id})")
            raise_not_found(detail="Fridge log not found")

        deleted = await self._crud.delete(data_id)
        if not deleted:
            self._log.logger.warning(f"failed delete fridge log id({data_id})")
            raise_bad_request()

        self._log.logger.info(f"success delete fridge log id({data_id})")
        return {"message": f"Fridge log {data_id} deleted successfully"}