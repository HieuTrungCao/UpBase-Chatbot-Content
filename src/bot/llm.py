import threading
import yaml

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

class GPTModel:
    __instance = None
    __lock = threading.Lock()

    def __init__(self):
        if GPTModel.__instance is not None:
            raise Exception("Only single graph created")
        
        with open("./config/system.yaml") as stream:
            self.config = yaml.safe_load(stream)

        self.llm = ChatOpenAI(
            model=self.config["llm"]["model"],
            temperature=self.config["llm"]["temperature"]
        )

    @staticmethod
    def get_instance():
        with GPTModel.__lock:
            if GPTModel.__instance is None:
                GPTModel.__instance = GPTModel()
            
            return GPTModel.__instance
        
    def invoke(self, prompt):
        return self.llm.invoke(prompt)
    
class GeminiModel:
    __instance = None
    __lock = threading.Lock()

    def __init__(self):
        if GeminiModel.__instance is not None:
            raise Exception("Only single graph created")
        
        with open("./config/system.yaml") as stream:
            self.config = yaml.safe_load(stream)

        self.llm = ChatGoogleGenerativeAI(
            model=self.config["llm"]["model"],
            temperature=self.config["llm"]["temperature"]
        )

    @staticmethod
    def get_instance():
        with GeminiModel.__lock:
            if GeminiModel.__instance is None:
                GeminiModel.__instance = GeminiModel()
            
            return GeminiModel.__instance
        
    def invoke(self, prompt):
        return self.llm.invoke(prompt)