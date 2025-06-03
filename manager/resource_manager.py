import cv2
import time
from core.singlebone_base import TFSingletonBase
from manager.tfconfig_manager import TFConfigManager as TFConfig
from core.tflog import TFLoggerManager as TFLog

class ResourceManager(TFSingletonBase):
    def __init__(self):
        if self._initialized:
            return
        
        super().__init__()
        self._log = TFLog.get_instance().get_logger()
        self._config = TFConfig.get_instance()
        
        self._init_video()

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


    def load_fridge_image(self) -> bytes:
        """
        이미지를 생성, JPEG 바이트로 반환
        """

        #resized = cv2.resize(image, (self._video_width, self._video_height))
        success, jpeg = cv2.imencode('.jpg', self._default_img)
        if not success:
            self._log.error(f"failed to encode image")
            return None

        return jpeg.tobytes()