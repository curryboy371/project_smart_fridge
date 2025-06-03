# api/chatgpt_router.py
import utils.exceptions
from api.routes_base import SimpleBaseAPI

from datetime import datetime

from manager.resource_manager import ResourceManager
from utils.validators import format_datetime
from fastapi.responses import StreamingResponse

from fastapi import FastAPI, UploadFile, File


class MainAPI(SimpleBaseAPI):
    def __init__(self):
        super().__init__("main")
        
        self._router.get("/", response_model=dict)(self.main_root)
        self._router.get("/time", response_model=dict)(self.main_time)
        self._router.get("/stream")(self.main_stream)
        self._router.get("/images")(self.main_image)
        

    # 서버 연결 체크
    async def main_root(self):
        return {"message": "Connected FastAPI Server!!!"}
    
    # 서버시간 반환
    async def main_time(self):
        now = datetime.now()
        return {"time": format_datetime(now, fmt="second"), 
                "hour": format_datetime(now, fmt="hour")
                }
    
    # 서버 스트리밍 반환
    def main_stream(self):
        return StreamingResponse(ResourceManager.get_instance().frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")

    # 이미지 반환
    async def main_image(self, files: UploadFile):
        
        
        results = []
        
        for file in files:
                content = await file.read()
                
                # 실제 저장: open(f"media/{file.filename}", "wb").write(content) 같은 식으로 가능
                results.append({"filename": file.filename, "size": len(content)})
        return {"uploaded": results}