import configparser
import os
from core.singlebone_base import TFSingletonBase

class TFConfigManager(TFSingletonBase):
    def __init__(self, config_path="config/config.ini"):
        if self._initialized:
            return
        
        self.config = configparser.ConfigParser()
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        self.config.read(config_path)
        self._initialized = True

    def get(self, section, key, fallback=None):
        return self.config.get(section, key, fallback=fallback)

    def getint(self, section, key, fallback=None):
        return self.config.getint(section, key, fallback=fallback)

    def getboolean(self, section, key, fallback=None):
        return self.config.getboolean(section, key, fallback=fallback)
    

config = TFConfigManager()
