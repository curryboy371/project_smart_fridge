from fastapi import FastAPI, APIRouter
from core import tfenums as en
from core.singlebone_base import TFSingletonBase

from api.routes_base import SimpleBaseAPI, BaseAPI
from api.routes_main import MainAPI
from api.routes_food_category import FoodCategoryAPI
from api.routes_user_profile import UserProfileAPI
from api.routes_fridge_item import FridgeItemAPI
from api.routes_fridge_log import FridgeLogAPI
from api.routes_chatgpt import ChatGPTAPI

from models.user_profile import UserProfileModel
from models.fridge_log import FridgeLogModel
from models.food_category import FoodCategoryModel
from models.fridge_item import FridgeItemModel

from crud.generic_crud import GenericCRUD
from crud.fridge_item_crud import FridgeItemCRUD

from models.model_base import SimpleModel
from crud.crud_manager import CrudManager


class RouterManager(TFSingletonBase):
    def __init__(self):
        if self._initialized:
            return
        super().__init__()
        
        self.routers = {}
        
        # Collection API Regist
        self._register_all()
        
        # Non Colllection API
        self.main_api = MainAPI()
        self.chatgpt_api = ChatGPTAPI()
        
  
    def _register_all(self):
        
        # main collection api, crud, model 세팅
        main_config_list = [
            (en.CollectionName.USER_PROFILE,   UserProfileAPI, UserProfileModel, GenericCRUD),
            (en.CollectionName.FRIDGE_ITEM,    FridgeItemAPI, FridgeItemModel, FridgeItemCRUD),
            (en.CollectionName.FRIDGE_LOG,     FridgeLogAPI, FridgeLogModel, GenericCRUD),
            (en.CollectionName.FOOD_CATEGORY,  FoodCategoryAPI, FoodCategoryModel, GenericCRUD),
         ]
        
        # simple collection api, crud, model 세팅
        simple_config_list = [
            (en.CollectionName.ALLERGIES,           BaseAPI, SimpleModel, GenericCRUD),
            (en.CollectionName.FOOD_SIMPLE_CATEGORY, BaseAPI, SimpleModel, GenericCRUD),
            (en.CollectionName.NUTRITION,           BaseAPI, SimpleModel, GenericCRUD),
            (en.CollectionName.STORAGE_METHOD,      BaseAPI, SimpleModel, GenericCRUD),
        ]
        
        # main collection list 등록    
        for col_enum, api_cls, model_cls, crud_cls in main_config_list:
            self._register_api(col_enum, api_cls, model_cls, crud_cls)
            
        # simple collection list 등록    
        for col_enum, api_cls, model_cls, crud_cls in simple_config_list:
            self._register_api(col_enum, api_cls, model_cls, crud_cls)
            
            
    def _register_api(self, collection_enum, api_class, model_class, crud_class):
        """
        API/CRUD/Model 등록
        """
        crudMgr = CrudManager.get_instance()
        
        api_instance = api_class(model_class, crud_class, collection_enum)  # api instalce 생성
        self.routers[collection_enum.value] = api_instance.router           # api router, router manager에 등록
        crudMgr.set_crud(collection_enum, api_instance.crud)           # crud, curd manager에 등록
        setattr(self, f"{collection_enum.name.lower()}_api", api_instance)  # api instance, router manager에 set
 

    def include_routers(self, app: FastAPI):
        
        #main router
        app.include_router(self.main_api.router)
        
        #gpt router
        app.include_router(self.chatgpt_api.router)

        # collection router
        for router in self.routers.values():
            app.include_router(router)