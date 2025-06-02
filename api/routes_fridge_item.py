from fastapi import APIRouter
from api.routes_base import BaseAPI
from models.fridge_item import FridgeItemModel
from typing import List

from typing import Optional
from datetime import datetime, timedelta

from api.routes_exception import *
from core import tfenums as en
from core.tflog import TFLoggerManager as TFLog

from crud.crud_manager import CrudManager

from fastapi import Query

class FridgeItemAPI(BaseAPI):
    def __init__(self, enum_value: en.CollectionName):
        super().__init__(model=FridgeItemModel, enum_value=enum_value)

        self._router.get("/expired", response_model=List[self._model])(self.get_expired_items)
        self._router.get("/expiring-soon", response_model=List[self._model])(self.get_expiring_soon_items)
        self._router.get("/{item_id}", response_model=self._model)(self.get_item)

        self._router.post("/", response_model=self._model)(self.create_item)
        self._router.post("/multiple", response_model=List[self._model])(self.create_items)
        self._router.put("/", response_model=self._model)(self.update_item)
        self._router.delete("/{item_id}")(self.delete_item)

    async def get_expired_items(self):
        return await self._crud.get_expired_items()
    
    async def get_expiring_soon_items(self, days: int = 1):
        now = datetime.now()
        limit = now + timedelta(days=days)
        return await self._crud.get_items_between_dates(now, limit)

    async def get_item(self, item_id: str):
        item = await self._crud.get_by_id(item_id)
        if not item:
            self._log.logger.warning(f"invalid fridge item id({item_id})")
            raise_not_found(detail="Fridge item not found")
        return item

    async def create_item(self, item: FridgeItemModel):
        item_id = item.id
        self._log.logger.info(f"try create fridge item id({item_id})")

        # 입고 날짜가 없다면 현재 시간으로 설정
        if item.entered_dt is None:
            item.entered_dt = datetime.utcnow()

        # food cateogy 정보 세팅팅
        food_category_crud = CrudManager.get_instance().get_crud(en.CollectionName.FOOD_CATEGORY)
        if food_category_crud:
            data = await food_category_crud.get_by_name(item.name)
            if data:
                item.food_category = data["food_category"]
                item.storageMethod = data["storageMethod"]

                # 유통기한이 없다면 카테고리 값 설정
                if item.expire_dt is None:
                    item.expire_dt = item.entered_dt + timedelta(days=data["shelfLifeDays"])

        created = await self._crud.create(item.dict(by_alias=True))
        if not created:
            self._log.logger.warning(f"failed create fridge item id({item_id})")
            raise_bad_request()

        # fridge log
        fridge_log_crud = CrudManager.get_instance().get_crud(en.CollectionName.FRIDGE_LOG)
        log_data = await CrudManager.get_instance().create_fridge_log_template(created, en.EventType.INBOUND)
        created_log = await fridge_log_crud.create(log_data)
        if not created_log:
            self._log.logger.error(f"failed create fridge log({item_id})")
        
        self._log.logger.info(f"success create fridge item id({item_id})")
        return created
    

    async def create_items(self, items: List[FridgeItemModel]):
        
        # 아이템을 리스트로 받는 경우는 입출고를 동시에 수행함
        # 기존의 아이템과 비교하는 절차가 수행되어야 함

        createds = []
        food_category_crud = CrudManager.get_instance().get_crud(en.CollectionName.FOOD_CATEGORY)

        for item in items:
            item_id = item.id
            self._log.logger.info(f"try create fridge item id({item_id})")

            # 입고 날짜가 없다면 현재 시간으로 설정
            if item.entered_dt is None:
                item.entered_dt = datetime.utcnow()

            # food cateogy 정보 세팅팅
            if food_category_crud:
                data = await food_category_crud.get_by_name(item.name)
                if data:
                    item.food_category = data["food_category"]
                    item.storageMethod = data["storageMethod"]

                    # 유통기한이 없다면 카테고리 값 설정
                    if item.expire_dt is None:
                        item.expire_dt = item.entered_dt + timedelta(days=data["shelfLifeDays"])

            created = await self._crud.create(item.dict(by_alias=True))
            if not created:
                self._log.logger.warning(f"failed create fridge item id({item_id})")
                raise_bad_request()

            # fridge log
            fridge_log_crud = CrudManager.get_instance().get_crud(en.CollectionName.FRIDGE_LOG)
            log_data = await CrudManager.get_instance().create_fridge_log_template(created, en.EventType.INBOUND)
            created_log = await fridge_log_crud.create(log_data)
            if not created_log:
                self._log.logger.error(f"failed create fridge log({item_id})")

            self._log.logger.info(f"success create fridge item id({item_id})")
            createds.append(created)
        
        return createds

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

        # fridge log
        fridge_log_crud = CrudManager.get_instance().get_crud(en.CollectionName.FRIDGE_LOG)
        log_data = await CrudManager.get_instance().create_fridge_log_template(item, en.EventType.DISCARDED)
        created_log = await fridge_log_crud.create(log_data)
        if not created_log:
            self._log.logger.error(f"failed create fridge log({item_id})")

        deleted = await self._crud.delete(item_id)
        if not deleted:
            self._log.logger.warning(f"failed delete fridge item id({item_id})")
            raise_bad_request()


        self._log.logger.info(f"success delete fridge item id({item_id})")
        return {"message": f"Fridge item {item_id} deleted successfully"}