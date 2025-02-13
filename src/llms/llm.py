import os
import threading

from openai import OpenAI
from dotenv import load_dotenv

class SingletonGPT:
    __instance = None
    __lock = threading.Lock()

    def __init__(self):
        if SingletonGPT.__instance is not None:
            raise Exception("Singleton GPT can only be instantaited once!")
        
        load_dotenv()
        self._openai_key = os.getenv("OPENAI_API_KEY")
        self.gpt = OpenAI(api_key=self._openai_key)

    @staticmethod
    def get_instance():
        with SingletonGPT.__lock():
            if SingletonGPT.__instance is None:
                SingletonGPT.__instance = SingletonGPT()
            return SingletonGPT.__instance