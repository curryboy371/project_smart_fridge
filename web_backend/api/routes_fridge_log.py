from fastapi import APIRouter
from api.routes_base import BaseAPI
from models.fridge_log import FridgeLogModel
from typing import List

from typing import Optional
from datetime import datetime, timedelta

import utils.exceptions
from core import tfenums as en

from typing import List, Type
from crud.fridge_log_crud import FridgeLogCRUD
from fastapi import Query
import utils.validators



class FridgeLogAPI(BaseAPI):
    def __init__(self, model, crud_class, enum_value):
        super().__init__(model, crud_class, enum_value)

        # API 경로 등록

        self._router.get("/event", response_model=List[self._model])(self.get_logs_by_event)
        self._router.get("/{id}", response_model=self._model)(self.get_datas)
        
        self._router.post("/", response_model=self._model)(self.create_data)
        self._router.put("/", response_model=self._model)(self.update_data)
        self._router.delete("/{id}")(self.delete_data)

    async def get_logs_by_event(self, event_type: str = Query(...)):
        return await self._crud.get_logs_by_event(event_type)

    async def get_datas(self):
        return await self._crud.get_all()
    
    async def create_data(self, data: FridgeLogModel):
        id = data.id
        self._log.logger.info(f"try create fridge log id({id})")

        if data.timestamp is None:
            formatted = utils.validators.format_datetime(datetime.utcnow(), fmt="second")
            data.timestamp = formatted
        else:
            utils.validators.validate_datetime_string(data.timestamp, fmt="second")

        created = await self._crud.create(data.dict(by_alias=True))
        if not created:
            self._log.logger.warning(f"failed create fridge log id({id})")
            utils.exceptions.raise_bad_request()

        self._log.logger.info(f"success create fridge log id({id})")
        return created

    async def update_data(self, data: FridgeLogModel):
        id = data.id
        self._log.logger.info(f"try update fridge log id({id})")

        updated = await self._crud.update(id, data.dict(by_alias=True))
        if not updated:
            self._log.logger.warning(f"failed update fridge log id({id})")
            utils.exceptions.raise_bad_request()

        self._log.logger.info(f"success update fridge log id({id})")
        return updated

    async def delete_data(self, id: str):
        self._log.logger.info(f"try delete fridge log id({id})")

        data = await self._crud.get_by_id(id)
        if not data:
            self._log.logger.warning(f"invalid fridge log id({id})")
            utils.exceptions.raise_not_found(detail="Fridge log not found")

        deleted = await self._crud.delete(id)
        if not deleted:
            self._log.logger.warning(f"failed delete fridge log id({id})")
            utils.exceptions.raise_bad_request()

        self._log.logger.info(f"success delete fridge log id({id})")
        return {"message": f"Fridge log {id} deleted successfully"}