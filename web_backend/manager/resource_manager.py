import cv2
import numpy as np
import os
from typing import Optional
from core.singlebone_base import TFSingletonBase
from manager.tfconfig_manager import TFConfigManager as TFConfig
from core.tflog import TFLoggerManager as TFLog
import asyncio

from manager.crud_manager import CrudManager
from crud.fridge_item_crud import FridgeItemCRUD
import core.tfenums as en
from pathlib import Path

class ResourceManager(TFSingletonBase):
    def __init__(self):
        if self._initialized:
            return
        
        super().__init__()
        self._log = TFLog.get_instance().get_logger()
        self._config = TFConfig.get_instance()
        self._proxy_frame = None
        self._stream_lock = asyncio.Lock()
        
        self._init_video()
        self._init_image()

    @property
    def proxy_frame(self):
        return self._proxy_frame
    
    @proxy_frame.setter
    def proxy_frame(self, value: bytes):
        self._proxy_frame = value

    def __del__(self):
        if self._video.isOpened():
            self._video.release()

    def _init_video(self):
        """
        비디오 관련 설정 및 캡처 객체 초기화
        """
        self._video_width = self._config.getint("resource", "video_width")
        self._video_height = self._config.getint("resource", "video_height")
        self._video_fps = self._config.getint("resource", "video_fps")
        video_path = self._config.get("resource", "video_path")

        self._video = cv2.VideoCapture(video_path)
        if not self._video.isOpened():
            self._log.error(f"failed open video: {video_path}")
            
    def _init_image(self):
        """
        이미지 관련 설정 및 디폴트 이미지 로드
        """
        default_img_path = self._config.get("resource", "default_img_path")
        self._img_path = self._config.get("resource", "img_path")
        self._img_width = self._config.getint("resource", "img_width")
        self._img_height = self._config.getint("resource", "img_height")

        default_img = cv2.imread(default_img_path)
        if default_img is None:
            self._log.error(f"failed open defualt img: {default_img_path}")
        else:
            self._default_img = cv2.resize(src=default_img, dsize=[self._img_width, self._img_height])
        

    async def frame_generator(self):
        """
        StreamingResponse에 사용되는 프레임 제너레이터
        """
        async with self._stream_lock:
            while True:
                success, frame = self._video.read()
                if not success:
                    self._video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
        
                resized = cv2.resize(frame, (self._video_width, self._video_height))
                _, jpeg = cv2.imencode('.jpg', resized)
                frame_bytes = jpeg.tobytes()

                yield (b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")
                await asyncio.sleep(1 / self._video_fps)


    async def proxy_frame_generator(self):
        """
        외부에서 받은 최신 프레임(self._last_frame)을 지속적으로 반환
        """
        async with self._stream_lock:
            while True:
                if self._proxy_frame:
                    yield (b"--frame\r\n"
                        b"Content-Type: image/jpeg\r\n\r\n" +
                        self._proxy_frame +
                        b"\r\n")
                await asyncio.sleep(1 / self._video_fps)

    async def load_fridge_image(self) -> Optional[bytes]:
        """
        냉장고 모든 자리가 채워져 있으면 composited.jpg, 비어 있으면 empty.jpg 반환
        """
        fridge_item_crud = CrudManager.get_instance().get_crud(en.CollectionName.FRIDGE_ITEM)

        bfridge_empty = True

        items = await fridge_item_crud.get_all()
        bfridge_empty = len(items) == 0
        
        img_path = Path("./resource/empty.jpg") if bfridge_empty else Path("./resource/composited.jpg")
        print(img_path)
        if not img_path.exists():
            self._log.error(f"Image file not found: {img_path}")
            return None

        image = cv2.imread(str(img_path))
        if image is None:
            self._log.error(f"Failed to load image from {img_path}")
            return None

        success, jpeg = cv2.imencode('.jpg', image)
        if not success:
            self._log.error("Failed to encode image to JPEG")
            return None

        return jpeg.tobytes()