# api/chatgpt_router.py
from api.routes_exception import *
from api.routes_base import SimpleBaseAPI

from datetime import datetime

from video.camera_manager import CameraManager
from core.tflog import TFLoggerManager as TFLog

from fastapi.responses import StreamingResponse
import cv2
import time



class MainAPI(SimpleBaseAPI):
    def __init__(self):
        super().__init__("main")
        
        self._router.get("/", response_model=dict)(self.main_root)
        self._router.get("/time", response_model=dict)(self.main_time)
        self._router.get("/stream")(self.main_stream)
        

    # 서버 연결 체크
    async def main_root(self):
        return {"message": "Connected FastAPI Server!!!"}
    
    # 서버시간 반환
    async def main_time(self):
        now = datetime.now()
        return {"time": now.strftime("%Y-%m-%d %H:%M:%S")}
    
    # 서버 스트리밍 반환
    def main_stream(self):
        return StreamingResponse(CameraManager.get_instance().frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")
