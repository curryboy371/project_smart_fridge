from motor.motor_asyncio import AsyncIOMotorClient
from core.singlebone_base import TFSingletonBase
from core.tflog import TFLoggerManager as TFLog
from core.tfconfig_manager import TFConfigManager as TFConfig
from core import tfenums as en
from core.tfenums import CollectionName

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
        
        # collection enum key로 세팅
        self.collections = {
            e: self.db[e.value] for e in en.CollectionName
        }
                
        
    async def create_collections(self):
        
        collection_list = [c.value for c in en.CollectionName]

        existing_collections = await self.db.list_collection_names()

        for collection in collection_list:
            if collection not in existing_collections:
                await self.db.create_collection(collection)
                logger.info(f"Created collection: {collection}")
            else:
                logger.info(f"Collection already exists: {collection}")

    async def is_connected(self):
        try:
            await self.client.admin.command('ping')
            return True
        except Exception as e:
            logger.critical("MongoDB 연결 실패:", e)
            return False
        
    def get_collection(self, name: en.CollectionName):
        
        if name not in self.collections:
            logger.error(f"invalid collection {name}")
            raise KeyError(f"Unknown collection key: {name}")
        
        return self.collections[name]
