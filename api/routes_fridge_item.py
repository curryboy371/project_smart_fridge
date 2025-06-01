from fastapi import APIRouter
from models.fridge_item import FridgeItemModel
from crud.generic_crud import GenericCRUD
from typing import List

from api.routes_exception import *
from core import tfenums as en
from core.tflog import TFLoggerManager as TFLog


class FridgeItemAPI():
    def __init__(self, enum_value: en.CollectionName):
        self._enum_value = enum_value
        self._log = TFLog.get_instance()
        self._crud = GenericCRUD(enum_value)  # GenericCRUD 사용, enum 값 넘겨서 초기화

        # API 경로 등록
        self._router = APIRouter(prefix=f"/{self._enum_value.value}")

        self._router.get("/", response_model=List[FridgeItemModel])(self.get_items)
        self._router.get("/{item_id}", response_model=FridgeItemModel)(self.get_item)
        self._router.post("/", response_model=FridgeItemModel)(self.create_item)
        self._router.put("/", response_model=FridgeItemModel)(self.update_item)
        self._router.delete("/{item_id}")(self.delete_item)

    @property
    def router(self):
        return self._router

    async def get_items(self):
        return await self._crud.get_all()

    async def get_item(self, item_id: str):
        item = await self._crud.get_by_id(item_id)
        if not item:
            self._log.logger.warning(f"invalid fridge item id({item_id})")
            raise_not_found(detail="Fridge item not found")
        return item

    async def create_item(self, item: FridgeItemModel):
        item_id = item.id
        self._log.logger.info(f"try create fridge item id({item_id})")

        created = await self._crud.create(item.dict(by_alias=True))
        if not created:
            self._log.logger.warning(f"failed create fridge item id({item_id})")
            raise_bad_request()

        self._log.logger.info(f"success create fridge item id({item_id})")
        return created

    async def update_item(self, item: FridgeItemModel):
        item_id = item.id
        self._log.logger.info(f"try update fridge item id({item_id})")

        updated = await self._crud.update(item_id, item.dict(by_alias=True))
        if not updated:
            self._log.logger.warning(f"failed update fridge item id({item_id})")
            raise_bad_request()

        self._log.logger.info(f"success update fridge item id({item_id})")
        return updated

    async def delete_item(self, item_id: str):
        self._log.logger.info(f"try delete fridge item id({item_id})")

        item = await self._crud.get_by_id(item_id)
        if not item:
            self._log.logger.warning(f"invalid fridge item id({item_id})")
            raise_not_found(detail="Fridge item not found")

        deleted = await self._crud.delete(item_id)
        if not deleted:
            self._log.logger.warning(f"failed delete fridge item id({item_id})")
            raise_bad_request()

        self._log.logger.info(f"success delete fridge item id({item_id})")
        return {"message": f"Fridge item {item_id} deleted successfully"}