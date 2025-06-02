from fastapi import FastAPI, APIRouter
from core import tfenums as en
from api.routes_exception import *
from core.singlebone_base import TFSingletonBase

from api.routes_simple import GetOnlyAPI
from api.routes_food_category import FoodCategoryAPI
from api.routes_user_profile import UserProfileAPI
from api.routes_fridge_item import FridgeItemAPI


from models.model_base import SimpleModel
from crud.crud_manager import CrudManager


class RouterManager(TFSingletonBase):
    def __init__(self):
        if self._initialized:
            return
        
        super().__init__()
        
        crudMgr = CrudManager.get_instance()

        self.routers = {}
        
        # TODO 좀 더 쉽게 초기화 할 수 있을까

        # 각 API 인스턴스 생성 (enum 타입 그대로 전달)
        evalue = en.CollectionName.FOOD_CATEGORY
        self.food_category_api = FoodCategoryAPI(evalue)
        self.routers[evalue.value] = self.food_category_api.router
        crudMgr.set_crud(evalue, self.food_category_api.crud)

        evalue = en.CollectionName.USER_PROFILE
        self.user_profile_api = UserProfileAPI(evalue)
        self.routers[evalue.value] = self.user_profile_api.router
        crudMgr.set_crud(evalue, self.user_profile_api.crud)

        evalue = en.CollectionName.FRIDGE_ITEM
        self.fridge_item_api = FridgeItemAPI(evalue)
        self.routers[evalue.value] = self.fridge_item_api.router
        crudMgr.set_crud(evalue, self.fridge_item_api.crud)

        evalue = en.CollectionName.ALLERGIES
        self.allergies_api = GetOnlyAPI(evalue, SimpleModel)
        self.routers[evalue.value] = self.allergies_api.router
        crudMgr.set_crud(evalue, self.allergies_api.crud)

        evalue = en.CollectionName.FOOD_SIMPLE_CATEGORY
        self.food_simple_category_api = GetOnlyAPI(evalue, SimpleModel)
        self.routers[evalue.value] = self.food_simple_category_api.router
        crudMgr.set_crud(evalue, self.food_simple_category_api.crud)

        evalue = en.CollectionName.NUTRITION
        self.nutrition_api = GetOnlyAPI(evalue, SimpleModel)
        self.routers[evalue.value] = self.nutrition_api.router
        crudMgr.set_crud(evalue, self.nutrition_api.crud)

        evalue = en.CollectionName.STORAGE_METHOD
        self.storage_method_api = GetOnlyAPI(evalue, SimpleModel)
        self.routers[evalue.value] = self.storage_method_api.router
        crudMgr.set_crud(evalue, self.storage_method_api.crud)
        

    def include_routers(self, app: FastAPI):
        
        for router in self.routers.values():
            app.include_router(router)
            print(f"include {router}")