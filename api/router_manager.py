from fastapi import FastAPI, APIRouter
from core import tfenums as en
from api.routes_exception import *
from core.singlebone_base import TFSingletonBase

from api.routes_simple import GetOnlyAPI
from api.routes_food_category import FoodCategoryAPI
from api.routes_user_profile import UserProfileAPI
from api.routes_fridge_item import FridgeItemAPI


from models.model_base import SimpleModel


class RouterManager(TFSingletonBase):
    def __init__(self):
        if self._initialized:
            return
        
        super().__init__()
        
        self.routers = {}
        
        # 각 API 인스턴스 생성 (enum 타입 그대로 전달)
        self.food_category_api = FoodCategoryAPI(en.CollectionName.FOOD_CATEGORY)
        self.routers[en.CollectionName.FOOD_CATEGORY.value] = self.food_category_api.router

        self.user_profile_api = UserProfileAPI(en.CollectionName.USER_PROFILE)
        self.routers[en.CollectionName.USER_PROFILE.value] = self.user_profile_api.router

        self.fridge_item_api = FridgeItemAPI(en.CollectionName.FRIDGE_ITEM)
        self.routers[en.CollectionName.FRIDGE_ITEM.value] = self.fridge_item_api.router


        self.allergies_api = GetOnlyAPI(en.CollectionName.ALLERGIES, SimpleModel)
        self.routers[en.CollectionName.ALLERGIES.value] = self.allergies_api.router

        self.food_simple_category_api = GetOnlyAPI(en.CollectionName.FOOD_SIMPLE_CATEGORY, SimpleModel)
        self.routers[en.CollectionName.FOOD_SIMPLE_CATEGORY.value] = self.food_simple_category_api.router

        self.nutrition_api = GetOnlyAPI(en.CollectionName.NUTRITION, SimpleModel)
        self.routers[en.CollectionName.NUTRITION.value] = self.nutrition_api.router
        
        self.food_simple_category_api = GetOnlyAPI(en.CollectionName.FOOD_SIMPLE_CATEGORY, SimpleModel)
        self.routers[en.CollectionName.FOOD_SIMPLE_CATEGORY.value] = self.food_simple_category_api.router

        self.storage_method_api = GetOnlyAPI(en.CollectionName.STORAGE_METHOD, SimpleModel)
        self.routers[en.CollectionName.STORAGE_METHOD.value] = self.storage_method_api.router

        self.nutrition_api = GetOnlyAPI(en.CollectionName.NUTRITION, SimpleModel)
        self.routers[en.CollectionName.NUTRITION.value] = self.nutrition_api.router

    def include_routers(self, app: FastAPI):
        
        for router in self.routers.values():
            app.include_router(router)
            print(f"include {router}")