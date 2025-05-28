import logging
from logging.handlers import RotatingFileHandler
import os

from core.singlebone_base import TFSingletonBase

"""
logger.debug("디버그 정보, 문제 분석용 상세 로그")
logger.info("일반 동작 정보, 사용자 액션 기록")
logger.warning("경고 메시지, 주의 필요")
logger.error("에러 발생, 예외 처리")
logger.critical("치명적 에러, 즉시 조치 필요")
"""

class TFLoggerManager(TFSingletonBase):

    def __init__(self, name="TF", log_dir="logs", log_file="server.log", max_bytes=5*1024*1024, backup_count=3):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        os.makedirs(log_dir, exist_ok=True)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # 콘솔 핸들러
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # 파일 핸들러
        file_handler = RotatingFileHandler(
            filename=os.path.join(log_dir, log_file),
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        
        # 중복 핸들러 추가 방지
        if not self.logger.hasHandlers():
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)
    
    def get_logger(self):
        return self.logger
    
    def set_level(self, level):
        self.logger.setLevel(level)
