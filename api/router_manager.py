from fastapi import FastAPI, APIRouter
from core import tfenums as en
from api.routes_exception import *
from core.singlebone_base import TFSingletonBase

from api.routes_base import SimpleBaseAPI, BaseAPI
from api.routes_main import MainAPI
from api.routes_food_category import FoodCategoryAPI
from api.routes_user_profile import UserProfileAPI
from api.routes_fridge_item import FridgeItemAPI
from api.routes_fridge_log import FridgeLogAPI
from api.routes_chatgpt import ChatGPTAPI


from models.model_base import SimpleModel
from crud.crud_manager import CrudManager


class RouterManager(TFSingletonBase):
    def __init__(self):
        if self._initialized:
            return
        
        super().__init__()
        
        crudMgr = CrudManager.get_instance()
        self.routers = {}
        
        # Non Colllection API
        self.main_api = MainAPI()
        self.chatgpt_api = ChatGPTAPI()
        
        # Model이 정해진 Collection
        main_collections = {
            en.CollectionName.USER_PROFILE: UserProfileAPI,
            en.CollectionName.FRIDGE_ITEM: FridgeItemAPI,
            en.CollectionName.FRIDGE_LOG: FridgeLogAPI,
            en.CollectionName.FOOD_CATEGORY: FoodCategoryAPI,
        }
        
        for evalue, APICls in main_collections.items():
            instance = APICls(evalue)
            self.routers[evalue.value] = instance.router
            crudMgr.set_crud(evalue, instance.crud)
            setattr(self, f"{evalue.name.lower()}_api", instance)

        # 공통 Model Simple Collection
        simple_collections = [
            en.CollectionName.ALLERGIES,
            en.CollectionName.FOOD_SIMPLE_CATEGORY,
            en.CollectionName.NUTRITION,
            en.CollectionName.STORAGE_METHOD,
        ]

        for evalue in simple_collections:
            api_instance = BaseAPI(SimpleModel, evalue)
            self.routers[evalue.value] = api_instance.router
            crudMgr.set_crud(evalue, api_instance.crud)
            setattr(self, f"{evalue.name.lower()}_api", api_instance)


    def include_routers(self, app: FastAPI):
        
        #main router
        app.include_router(self.main_api.router)
        
        #gpt router
        app.include_router(self.chatgpt_api.router)

        # collection router
        for router in self.routers.values():
            app.include_router(router)