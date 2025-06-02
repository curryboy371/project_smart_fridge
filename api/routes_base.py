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

# Crud를 사용 안하는 API
class SimpleBaseAPI:
    def __init__(self, tag: str):
        self._log = TFLog.get_instance()
        self._tag = tag
        prefix = f"/{self._tag}"
        self._router = APIRouter(prefix=prefix, tags=[self._tag])
        
    @property
    def router(self):
        return self._router

# Crud를 사용하는 API
class BaseAPI:
    def __init__(self, model: Type[TFBaseMdoel], enum_value: en.CollectionName, tag: str = None):
        self._model = model
        self._enum_value = enum_value
        self._log = TFLog.get_instance()
        self._crud = GenericCRUD(enum_value)

        self._tag = self._enum_value.value if not tag else tag
        prefix = f"/{self._enum_value.value}"
        self._router = APIRouter(prefix=prefix, tags=[self._tag])

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
