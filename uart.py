import asyncio
import serial
import threading


class SerialReader:
    def __init__(self, port='/dev/serial0', baudrate=115200, loop=None):
        
        self.serial = serial.Serial(     # serial 객체 생성
        port=port,                       # 시리얼통신에 사용할 포트
        baudrate=baudrate,               # 통신속도 지정
        parity=serial.PARITY_NONE,       # 패리티 비트 설정방식
        stopbits=serial.STOPBITS_ONE,    # 스톱비트 지정
        bytesize=serial.EIGHTBITS,       # 데이터 비트수 지정
        timeout=1                        # 타임아웃 설정
        )
        self._running = True
        self._loop = loop
        self.thread = threading.Thread(target=self._read_loop, daemon=True)
        self._detect_callback = None  # 콜백 함수 저장용


    def start(self):
        if not self.thread.is_alive():
            self.thread.start()


    def _read_loop(self):
        while self._running:
            if self.serial.in_waiting > 0:
                msg = self.serial.readline().decode('utf-8', errors='ignore').strip()
                print("Received:", msg)
                if msg == "d" and self._detect_callback:
                    if asyncio.iscoroutinefunction(self._detect_callback):
                        asyncio.run_coroutine_threadsafe(self._detect_callback(), self._loop)
                    else:
                        self._detect_callback()

    def callback(self):
        if asyncio.iscoroutinefunction(self._detect_callback):
            asyncio.run_coroutine_threadsafe(self._detect_callback(), self._loop)
        else:
            self._detect_callback()
    
    
    def send(self, message: str):
        if self.serial.is_open:
            print("send : ")
            self.serial.write((message + "\n").encode('utf-8'))

    def set_detect_callback(self, func):
        """'uart 수신시 detect 기능을 수행하기 위한 callback."""
        self._detect_callback = func
        print("set detect callback")

    def stop(self):
        self._running = False
        self.thread.join()
        self.serial.close()
        print("[INFO] SerialReader stopped")
