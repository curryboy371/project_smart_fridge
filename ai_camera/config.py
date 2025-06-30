from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# default info
WIDTH = int(os.getenv("WIDTH", 640))
HEIGHT = int(os.getenv("HEIGHT", 480))
VIDEO_FPS = int(os.getenv("VIDEO_FPS", 480))

# detect info
YOLO_MODEL_PATH = os.getenv("YOLO_MODEL_PATH")
CAMERA_WINDOW_NAME = os.getenv("CAMERA_WINDOW_NAME")
CONFIDENCE = float(os.getenv("CONFIDENCE", 0.5)) 

COMPOS_IMG_PATH = os.getenv("COMPOS_IMG_PATH")

# api info
API_HOST = os.getenv("API_HOST")
API_PORT = os.getenv("API_PORT")
API_POST_ITEMS = os.getenv("API_POST_ITEMS")
API_RECV_FRAME = os.getenv("API_RECV_FRAME")
API_RECV_FRAME = os.getenv("API_RECV_FRAME")
API_RECV_IMAGE = os.getenv("API_RECV_IMAGE")

API_POST_ITEMS_URL = f"{API_HOST}:{API_PORT}{API_POST_ITEMS}"
API_STREAM_URL = f"{API_HOST}:{API_PORT}{API_RECV_FRAME}"
API_IMAGE_URL = f"{API_HOST}:{API_PORT}{API_RECV_IMAGE}"


# Serial info
SERIAL_PORT = os.getenv("SERIAL_PORT", "/dev/serial0")
SERIAL_BAUDRATE = int(os.getenv("SERIAL_BAUDRATE", 9600))