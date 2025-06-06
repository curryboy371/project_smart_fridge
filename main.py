
import api
import config
from datetime import datetime
import time

import camera_manager
import asyncio

import uart

import cv2

camera_mgr = camera_manager.CameraManager()
server_api = api.WebServerAPI()


async def detect():
    print("객체 탐지 시작")
    result = await camera_mgr.detect_objects()
    await server_api.send_items(result)
    await server_api.send_image()
        
async def main():
    loop = asyncio.get_running_loop()
    serial_reader = uart.SerialReader(baudrate=config.SERIAL_BAUDRATE, port=config.SERIAL_PORT, loop=loop)
    serial_reader.set_detect_callback(detect)
    serial_reader.start()

    # 카메라 프레임 루프를 비동기로 실행
    
    camera_task = asyncio.create_task(camera_mgr.run())
    try:
        while True:
            
            await server_api.send_frame(camera_mgr.get_stream_frame())
            
            # key = cv2.waitKey(5) & 0xFF
            # if key == ord('q'):
            #     print("종료")
            #     break
            # elif key == ord('w'):
            #     serial_reader.callback()
            await asyncio.sleep(0.01)  # CPU 점유율 방지

    except asyncio.CancelledError:
        print("asyncio error")
    finally:
        print("exit...")
        camera_task.cancel()
        serial_reader.stop()
        camera_mgr.release_camera()
        cv2.destroyAllWindows()
        
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("키보드 종료")