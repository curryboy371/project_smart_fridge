# api/chatgpt_router.py
import utils.exceptions
from api.routes_base import SimpleBaseAPI

from datetime import datetime

from manager.resource_manager import ResourceManager
from utils.validators import format_datetime
from fastapi.responses import StreamingResponse
from fastapi import Response
import utils.exceptions
from fastapi import UploadFile, File
import asyncio
from pathlib import Path
import shutil

from manager.tfconfig_manager import TFConfigManager as TFConfig


class MainAPI(SimpleBaseAPI):
    def __init__(self):
        super().__init__("main")
        
        # Raspberry Pi 스트리밍 URL
        config = TFConfig.get_instance()
        self._RPI_STREAM_URL = config.get("raspberry", "stream_url")
        self._last_frame = None

        self._router.get("/", response_model=dict)(self.main_root)
        self._router.get("/time", response_model=dict)(self.main_time)
        self._router.get("/image")(self.main_image)
        self._router.get("/stream")(self.main_stream_local)
        self._router.get("/proxy_stream")(self.main_stream_proxy)

        self._router.post("/recv_frame")(self.receive_frame)
        self._router.post("/recv_image")(self.receive_image)
        

    # 서버 연결 체크
    async def main_root(self):
        return {"message": "Connected FastAPI Server!!!"}
    
    # 서버시간 반환
    async def main_time(self):
        now = datetime.now()
        return {"time": format_datetime(now, fmt="second"), 
                "hour": format_datetime(now, fmt="hour")
                }
    
    # ras 프록시를 통해 frame 얻어서 저장
    async def receive_frame(self, image: UploadFile):
        ResourceManager.get_instance().proxy_frame = await image.read()  # 파일 내용을 메모리에 저장
        return {"status": "received"}
    
    
    # ras에서 이미지 얻음
    async def receive_image(self, file: UploadFile = File(...)):
        
        save_path = Path("resource/composited.jpg")
        save_path.parent.mkdir(parents=True, exist_ok=True)

        with save_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {"status": "success", "path": save_path}

    # 프록시 스트리밍 반환 ( frame to Web)
    async def main_stream_proxy(self):
        return StreamingResponse(ResourceManager.get_instance().proxy_frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")

    # 서버 스트리밍 반환 ( 서버 로컬 영상 )
    async def main_stream_local(self):
        return StreamingResponse(ResourceManager.get_instance().frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")

    # 이미지 반환
    async def main_image(self):
        image = await ResourceManager.get_instance().load_fridge_image()
        if image is None:
            utils.exceptions.raise_bad_request(detail="image is none")
            
        return Response(content=image, media_type="image/jpeg")
    
    
