from motor.motor_asyncio import AsyncIOMotorClient
from core.singlebone_base import TFSingletonBase
from core.tflog import TFLoggerManager as TFLog
from core.tfconfig_manager import TFConfigManager as TFConfig

logger = TFLog.get_instance().get_logger()

class TFDB(TFSingletonBase):
    def __init__(self):
        if self._initialized:
            return
        
        super().__init__()
        self._init_database()

    def _init_database(self):
        configger = TFConfig.get_instance()
        hostname = configger.get("database", "host")
        port = configger.getint("database", "port")
        dbname = configger.get("database", "name")
        uri = f'mongodb://{hostname}:{port}'

        logger.info(f"DB URI : {uri}")

        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[dbname]

        # db collection 
        self.user_collection = self.db.users
        self.user_profile_collection = self.db.user_profile
        self.food_category_collection = self.db.food_category
        self.fridge_item_collection = self.db.fridge_item


    async def is_connected(self):
        try:
            await self.client.admin.command('ping')
            return True
        except Exception as e:
            logger.critical("MongoDB 연결 실패:", e)
            return False
