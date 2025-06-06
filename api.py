# send_data.py
import requests
import config
from typing import List
from datetime import datetime
import asyncio


class WebServerAPI:
    def __init__(self):
        self._items_url = config.API_POST_ITEMS_URL
        self._stream_url = config.API_STREAM_URL
        self._image_url = config.API_IMAGE_URL
        

    async def send_items(self, items: List[dict]) -> bool:
        try:
            response = requests.post(self._items_url, json=items)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return False
        
    async def send_frame(self, img_bytes: bytes):
        try:
            response = requests.post(
                self._stream_url,
                files={"image": ("frame.jpg", img_bytes, "image/jpeg")},
                timeout=2.0
            )
            if response.status_code != 200:
                print(f"서버 응답 오류: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"전송 실패: {e}")
            await asyncio.sleep(5)

    async def send_image(self):
        with open(config.COMPOS_IMG_PATH, "rb") as f:
            files = {"file": (config.COMPOS_IMG_PATH, f, "image/jpeg")}
            try:
                response = requests.post(self._image_url, files=files, timeout=5)
                response.raise_for_status()
                print(f"Status: {response.json()}")
            except requests.RequestException as e:
                print(f"Request Failed: {e}")

