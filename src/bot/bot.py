import threading

from .llm import GPTModel
from .graph import ContentGraph, ModifierGraph

class Bot:
    __instance = None
    __lock = threading.Lock()

    def __init__(self):
        if Bot.__instance is not None:
            raise Exception("Only sighle bot created")
        
        self.llm = GPTModel()
        self.content_agent = ContentGraph(self.llm, prompt_file="config/prompt.yaml", hook_file="resource/hook.yaml")
        self.content_agent.graph_builder()

        self.moodifier_agent = ModifierGraph(self.llm, prompt_modifier_file="config/prompt.yaml")
        self.moodifier_agent.graph_builder()

    @staticmethod
    def get_instance():
        with Bot.__lock:
            if Bot.__instance is None:
                Bot.__instance = Bot()
            
            return Bot.__instance
        
    def generate_content(self, structure, style, description, hook):

        for chunk in self.content_agent.graph.stream({
                "structure": structure,
                "style": style,
                "description": description,
                "hook_sample": hook
            }):
            
            return chunk["content_generator"]["content"]
        
    def modify_content(self, content, content_feedback):
        for content in self.moodifier_agent.graph.stream({
                "feedback": content_feedback,
                "content": content
            },
            {"configurable": {"thread_id": "1"}}):
        
            return content["content_modifier"]["modified_content"]