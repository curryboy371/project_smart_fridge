# api/chatgpt_router.py
from api.routes_exception import *
from api.routes_base import SimpleBaseAPI

from datetime import datetime

from core.tflog import TFLoggerManager as TFLog

class MainAPI(SimpleBaseAPI):
    def __init__(self):
        super().__init__("main")
        
        self._router.get("/", response_model=dict)(self.root_main)
        self._router.get("/time", response_model=dict)(self.root_time)



    async def root_main(self):
        return {"message": "Connected FastAPI Server!!!"}
    
    async def root_time(self):
        now = datetime.now()
        return {"time": now.strftime("%Y-%m-%d %H:%M:%S")}



