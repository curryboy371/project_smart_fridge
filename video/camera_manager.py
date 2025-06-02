import cv2
import time
from core.singlebone_base import TFSingletonBase
from core.tfconfig_manager import TFConfigManager as TFConfig
from core.tflog import TFLoggerManager as TFLog

class CameraManager(TFSingletonBase):
    def __init__(self):
        if self._initialized:
            return
        
        super().__init__()
        
        self._log = TFLog.get_instance().get_logger()
        config = TFConfig.get_instance()

        self._video_width = config.getint("video", "width")
        self._video_height = config.getint("video", "height")
        self._video_fps = config.getint("video", "fps")
        video_path = config.get("video", "path")

        #video load
        self._video = cv2.VideoCapture(video_path)
        if not self._video.isOpened():
            self._log.error(f"failed open video: {video_path}")
    
    def __del__(self):
        if self._video.isOpened():
            self._video.release()

    def frame_generator(self):
        """
        StreamingResponse에 사용되는 프레임 제너레이터
        """
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
            time.sleep(1 / self._video_fps)
