import threading

from langchain_openai import ChatOpenAI

class GPTModel:
    __instance = None
    __lock = threading.Lock()

    def __init__(self, model_name="gpt-4o"):
        if GPTModel.__instance is not None:
            raise Exception("Only single graph created")
        self.llm = ChatOpenAI(model=model_name)

    @staticmethod
    def get_instance(model_name="gpt-4o"):
        with GPTModel.__lock:
            if GPTModel.__instance is None:
                GPTModel.__instance = GPTModel(model_name=model_name)
            
            return GPTModel.__instance
        
    def invoke(self, prompt):
        return self.llm.invoke(prompt)