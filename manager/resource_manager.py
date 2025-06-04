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
        이미지를 생성, JPEG 바이트로 반환
        """

        #냉장고 상황 확인
        fridge_item_crud = CrudManager().get_instance().get_crud(en.CollectionName.FRIDGE_ITEM)
        image_grid = []
        

        
        for i in range(en.FridgePosition.MAX.value):
            item = await fridge_item_crud.get_position_item(i)

            # 이미지 존재 여부 확인
            filename = f"{i}.jpg"
            filepath = os.path.join(self._img_path, filename)
            if item and self._img_path and os.path.exists(filepath):
                img = cv2.imread(filepath)
            else:
                img = self._default_img
                print(f"Default image used for position {i}")
                            
            if img is None:
                self._log.error(f"image load fail: position={i}")
                img = np.ones((240, 320, 3), dtype=np.uint8) * 200  # 완전한 fallback 이미지
            
                
            # 리사이즈
            resized = cv2.resize(img, (320, 240))
            image_grid.append(resized)
            
        
        # 2행 2열로 합치기
        top_row = np.hstack((image_grid[0], image_grid[1]))  # 좌상 + 우상
        bottom_row = np.hstack((image_grid[2], image_grid[3]))  # 좌하 + 우하
        combined = np.vstack((top_row, bottom_row))  # 위아래 붙이기
        
        
        # 십자 경계선 그리기
        h, w = combined.shape[:2]
        center_x = w // 2
        center_y = h // 2
        
        cv2.line(combined, (center_x, 0), (center_x, h), (0, 0, 255), thickness=4)
        cv2.line(combined, (0, center_y), (w, center_y), (0, 0, 255), thickness=4)
        
        # JPEG 인코딩
        success, jpeg = cv2.imencode('.jpg', combined)
        if not success:
            self._log.error("fail image encoding")
            return None

        return jpeg.tobytes()