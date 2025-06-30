
class TFSingletonBase:
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__new__(cls)
            instance._initialized = False
            cls._instances[cls] = instance
        return cls._instances[cls]

    def __init__(self, *args, **kwargs):
        if self._initialized:
            return
        # initialize
        self._initialized = True

    @classmethod
    def get_instance(cls, *args, **kwargs):
        return cls(*args, **kwargs)