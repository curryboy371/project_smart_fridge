from ultralytics import YOLO
import cv2 as cv2
from pathlib import Path
import config

import numpy as np
import asyncio

class CameraManager:
    def __init__(self, input_source=0):
        self.input_source = input_source
        
        self.model_path = Path(config.YOLO_MODEL_PATH)
        self.window_name = config.CAMERA_WINDOW_NAME
        self.width = config.WIDTH
        self.height = config.HEIGHT
        self.fps = config.VIDEO_FPS
        self.model = None
        self.cap = None
        
        self.last_frame = None
        
        self.detected_objects = []

        self._load_model()
        self._open_camera()
            
    def release_camera(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
                

    def _load_model(self):
        if not self.model_path.is_file():
            raise FileNotFoundError(f"Failed Find Model {self.model_path}")
        self.model = YOLO(self.model_path)
        self.conf_threshold = config.CONFIDENCE
        self.model.conf = self.conf_threshold
        print(f"Model Load: {self.model_path.resolve()}")

    def _open_camera(self):
        self.cap = cv2.VideoCapture(self.input_source)
        if not self.cap.isOpened():
            raise RuntimeError(f"Failed Video Open (ID: {self.input_source})")
        print(f"Open Video (ID: {self.input_source})")
        
    
    async def save_cropped_image(self, image: np.ndarray, position: int):
        save_path = Path(f"./detected/{position}.jpg")
        save_path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(save_path), image)

    def get_stream_frame(self) -> np.ndarray:
        if self.last_frame is not None and self.last_frame.size > 0:
            _, jpeg = cv2.imencode('.jpg', self.last_frame)
            encoded_frame = jpeg.tobytes()
            return encoded_frame
        return b''
    
    async def compose_and_save_cropped_images(self, position_map: dict[int, np.ndarray]):
        # 각 포지션 음식을 한장의 캔버스로
        canvas_size = (self.height * 2, self.width * 2, 3)  # (H x 2, W x 2)
        canvas = np.zeros(canvas_size, dtype=np.uint8) 

        # 4분할
        for pos in range(4):
            row = pos // 2
            col = pos % 2
            y_offset = row * self.height
            x_offset = col * self.width

            if pos in position_map:
                resized = cv2.resize(position_map[pos], (self.width, self.height))
                canvas[y_offset:y_offset + self.height, x_offset:x_offset + self.width] = resized

        # 십자가 표시
        draw_center_cross(canvas)

        save_path = Path("./detected/composited.jpg")
        save_path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(save_path), canvas)
        
    
    # 객체 탐지
    async def detect_objects(self) -> np.ndarray:
        self.detected_objects.clear()
        frame = self.last_frame
        results = self.model(frame)
        frame_height, frame_width = frame.shape[:2]
        
        position_map = {}
        
        for box in results[0].boxes:
            
            #확률 얻어서 특정 확률 이상의 객체만 탐지
            conf = float(box.conf[0])
            if conf < self.conf_threshold:
                continue
            
            xyxy = box.xyxy[0].cpu().numpy().astype(int)
            cls = int(box.cls[0])
            
            # 객체 왼쪽, 객체 위쪽, 객체 오른쪽, 객체 아래쪽
            x1, y1, x2, y2 = xyxy
            cropped = frame[y1:y2, x1:x2]

            # 객체 위치를 전달하여 포지션 설정
            position = get_position(x1, y1, x2, y2, frame_width, frame_height)
            position_map[position] = cropped 

            self.detected_objects.append({
                "name": self.model.names[cls],
                "position": position
            })
            

        await self.compose_and_save_cropped_images(position_map)
        
        return self.detected_objects
    

    async def run(self):
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("Frame Load Failed")
                    break

                frame = cv2.resize(frame, (self.width, self.height))
                self.last_frame = frame
                
                # 위치 분할 십자
                draw_center_cross(frame)

                cv2.imshow(self.window_name, frame)
                await asyncio.sleep(1 / self.fps)

        except Exception as e:
            print(f"[Camera Manager Error] {e}")
        finally:
            self.release_camera()


def draw_center_cross(frame: np.ndarray, color=(0, 0, 255), thickness=2) -> None:
    """
    주어진 프레임의 중앙에 십자선을 그림
    """
    height, width = frame.shape[:2]
    center_x = width // 2
    center_y = height // 2
    cv2.line(frame, (center_x, 0), (center_x, height), color, thickness)
    cv2.line(frame, (0, center_y), (width, center_y), color, thickness)


def get_position(x1, y1, x2, y2, frame_width, frame_height):
    """
    중심 좌표를 기준 4분할하여 포지션 인덱스 반환 
    0 1
    2 3
    """
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2

    col = 0 if center_x < frame_width / 2 else 1
    row = 0 if center_y < frame_height / 2 else 1
    return row * 2 + col


if __name__ == "__main__":
    cam_mgr = CameraManager()
    asyncio.run(cam_mgr.run())
    