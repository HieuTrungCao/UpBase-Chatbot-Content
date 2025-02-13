import lark_oapi as lark
import os
import threading

from dotenv import load_dotenv

class SingletonLark:
    __instance = None
    __lock = threading.Lock()

    def __init__(self):
        if SingletonLark.__instance is not None:
            raise Exception("Singleton Client can only be instantiated once!")
        load_dotenv()
        self._app_id = os.getenv("APP_ID")
        self._app_secret = os.getenv("APP_SECRET")        
        self.client = lark.Client.builder()\
            .app_id(self._app_id)\
            .app_secret(self._app_secret)\
            .log_level(lark.LogLevel.DEBUG)\
            .build()

    @staticmethod
    def get_instance():
        with SingletonLark.__lock:
            if SingletonLark.__instance is None:
                SingletonLark.__instance = SingletonLark()
            return SingletonLark.__instance
            