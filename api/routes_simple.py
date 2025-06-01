from fastapi import APIRouter
from typing import List

from api.routes_exception import *
from core.tfdb import CollectionName

from fastapi import APIRouter
from typing import List, Type
from pydantic import BaseModel
from crud.generic_crud import GenericCRUD
from api.routes_exception import *
from core.tflog import TFLoggerManager as TFLog

class GetOnlyAPI:
    def __init__(self, enum_value: CollectionName, model: Type[BaseModel]):
        self._enum_value = enum_value
        self._model = model
        self._log = TFLog.get_instance()
        self._crud = GenericCRUD(enum_value)

        self._router = APIRouter(prefix=f"/{self._enum_value.value}")

        # GET 라우터만 등록
        self._router.get("/", response_model=List[self._model])(self.get_all)

    @property
    def router(self):
        return self._router

    async def get_all(self):
        return await self._crud.get_all()