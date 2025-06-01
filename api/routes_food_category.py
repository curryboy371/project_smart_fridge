from fastapi import APIRouter
from typing import List
from models.food_category import FoodCategoryModel
from crud.generic_crud import GenericCRUD
from api.routes_exception import *
from core.tflog import TFLoggerManager as TFLog
from core import tfenums as en

class FoodCategoryAPI():
    def __init__(self, enum_value: en.CollectionName):
        self._enum_value = enum_value
        self._log = TFLog.get_instance()
        self._crud = GenericCRUD(enum_value)  # enum 값 넘겨서 초기화

        self._router = APIRouter(prefix=f"/{self._enum_value.value}")

        self._router.get("/", response_model=List[FoodCategoryModel])(self.get_categories)
        self._router.get("/{category_id}", response_model=FoodCategoryModel)(self.get_category)
        self._router.post("/", response_model=FoodCategoryModel)(self.create_category)
        self._router.put("/", response_model=FoodCategoryModel)(self.update_category)
        self._router.delete("/{category_id}")(self.delete_category)


    @property
    def router(self):
        return self._router
    
    async def get_categories(self):
        return await self._crud.get_all()

    async def get_category(self, category_id: str):
        category = await self._crud.get_by_id(category_id)
        if not category:
            raise_not_found()
        return category

    async def create_category(self, category: FoodCategoryModel):
        created = await self._crud.create(category.dict(by_alias=True))
        if not created:
            raise_bad_request()
        return created

    async def update_category(self, category: FoodCategoryModel):
        updated = await self._crud.update(category.id, category.dict(by_alias=True))
        if not updated:
            raise_bad_request()
        return updated

    async def delete_category(self, category_id: str):
        deleted = await self._crud.delete(category_id)
        if not deleted:
            raise_bad_request()
        return {"message": f"Category {category_id} deleted successfully"}