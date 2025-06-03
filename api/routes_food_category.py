from fastapi import APIRouter
from api.routes_base import BaseAPI
from models.food_category import FoodCategoryModel
import utils.exceptions
from core import tfenums as en


class FoodCategoryAPI(BaseAPI):
    def __init__(self, model, crud_class, enum_value):
        super().__init__(model, crud_class, enum_value)

        #base overriding
        self._router.get("/{id}", response_model=self._model)(self.get_categories)
        self._router.post("/", response_model=self._model)(self.create_category)
        self._router.put("/", response_model=self._model)(self.update_category)
        self._router.delete("/{id}")(self.delete_category)
  
    async def get_categories(self):
        return await self._crud.get_all()
    
  
    async def create_category(self, category: FoodCategoryModel):
        # 중복 체크
        existing = await self._crud.get_by_name(category.name)
        if existing:
            self._log.logger.info(f"duplicate {category.name}")
            utils.exceptions.raise_conflict(detail="exist category name")

        created = await self._crud.create(category.dict(by_alias=True))
        if not created:
            utils.exceptions.raise_bad_request()
            
        self._log.logger.info(f"Category {category.id} create successfully")
        return created

    async def update_category(self, category: FoodCategoryModel):
        # 중복 체크
        id = category.id
        existing_id = await self._crud.get_by_id(id)
        if not existing_id:
            self._log.logger.info(f"invalid id {id}")
            utils.exceptions.raise_bad_request(detail="invalid id")
        
        existing_name = await self._crud.get_by_name(category.name)
        if existing_name:
            obj_id = existing_name["_id"]
            if obj_id != category.id: # 기존에 있는 name으로 교체한 경우 중복
                self._log.logger.info(f"duplicate {category.name}")
                utils.exceptions.raise_conflict(detail="exist category name")
        
        updated = await self._crud.update(category.id, category.dict(by_alias=True))
        if not updated:
            utils.exceptions.raise_bad_request()
            
        self._log.logger.info(f"Category {category.id} update successfully")    
        return updated

    async def delete_category(self, id: str):
        deleted = await self._crud.delete(id)
        if not deleted:
            utils.exceptions.raise_bad_request()
        return {"message": f"Category {id} deleted successfully"}