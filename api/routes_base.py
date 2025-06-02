# api/base_api.py
from fastapi import APIRouter
from typing import List, Type
from pydantic import BaseModel
from core.tflog import TFLoggerManager as TFLog
from api.routes_exception import *
from crud.generic_crud import GenericCRUD
from core import tfenums as en
from typing import Optional
from models.model_base import TFBaseMdoel

class SimpleBaseAPI:
    def __init__(self, tag: str):
        self._log = TFLog.get_instance()
        self._tag = tag
        prefix = f"/{self._tag}"
        self._router = APIRouter(prefix=prefix, tags=[self._tag])

    @property
    def router(self):
        return self._router

class BaseAPI:
    def __init__(self, model: Type[TFBaseMdoel], enum_value: en.CollectionName, tag: str = None):
        self._model = model
        self._enum_value = enum_value
        self._log = TFLog.get_instance()
        self._crud = GenericCRUD(enum_value)

        self._tag = f"/{self._enum_value.value}" if not tag else tag
        self._router = APIRouter(prefix=self._tag, tags=[self._enum_value.value])

        self._router.get("/", response_model=List[self._model])(self.get_all)

        # 자식에서 다시 등록하면 충돌나서 제대로 동작 안함
        # 오버라이딩 해야하는 주소가 하나라도 있으면 Base에서 등록 금지
        #self._router.get("/{item_id}", response_model=self._model)(self.get_by_id)
        #self._router.post("/", response_model=self._model)(self.create)
        #self._router.put("/", response_model=self._model)(self.update)
        #self._router.delete("/{item_id}")(self.delete)

    @property
    def router(self):
        return self._router

    @property
    def crud(self):
        return self._crud

    async def get_all(self):
         return await self._crud.get_all()

    # async def get_by_id(self, item_id: str):
    #     item = await self._crud.get_by_id(item_id)
    #     if not item:
    #         raise_not_found()
    #     return item

    # async def create(self, item: TFBaseMdoel):
    #     self._log.logger.info(f"[{self._tag}] Try create {item.id}")
    #     created = await self._crud.create(item.dict(by_alias=True))
    #     if not created:
    #         raise_bad_request()

    #     self._log.logger.info(f"[{self._tag}] create {item.id}")
    #     return created

    # async def update(self, item: TFBaseMdoel):
    #     self._log.logger.info(f"[{self._tag}] Try update {item.id}")
    #     existing = await self._crud.get_by_id(item.id)
    #     if not existing:
    #         raise_bad_request(detail="Invalid ID")

    #     updated = await self._crud.update(item.id, item.dict(by_alias=True))
    #     if not updated:
    #         raise_bad_request()

    #     self._log.logger.info(f"[{self._tag}] update {item.id}")
    #     return updated

    # async def delete(self, item_id: str):
    #     self._log.logger.info(f"[{self._tag}] Try delete {item_id}")
    #     deleted = await self._crud.delete(item_id)
    #     if not deleted:
    #         raise_bad_request()

    #     self._log.logger.info(f"[{self._tag}] delete {item_id}")
    #     return {"message": f"Item {item_id} deleted successfully"}