from .resp_queue import SingletonQueue
from src.constants import CALL_OPENAI

resp_queue = SingletonQueue.get_instance()

def call_llm():
    while True:
        try:
            response = resp_queue.get(timeout=1)
            if response[0] >= 0:
                response[-1](response[1])
        except:
            pass