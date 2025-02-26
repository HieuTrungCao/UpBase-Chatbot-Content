import threading

from typing import List

class ContentList:
    __instance = None
    __lock = threading.Lock()

    def __init__(self):
        if ContentList.__instance is not None:
            raise Exception("Only sighle bot created")
        
        self.contents: List[str] = []

    @staticmethod
    def get_instance():
        with ContentList.__lock:
            if ContentList.__instance is None:
                ContentList.__instance = ContentList()
            
            return ContentList.__instance
        
    def get_content(self) -> str:
        return self.contents[-1]

    def put_content(self, content):
        self.contents.append(content)

    def length(self):
        return len(self.contents)