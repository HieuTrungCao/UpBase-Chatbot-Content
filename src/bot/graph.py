import threading
import yaml

from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langchain_core.language_models import BaseChatModel
from langgraph.checkpoint.memory import MemorySaver

from .state import (
    ContentState,
    HookState,
    IntroState,
    MainState,
    EndState,
    ModifierState,
    CheckerState
)

class ContentGraph:
    __instance = None
    __lock = threading.Lock()

    def __init__(self, llm = None, prompt_file = None, hook_file = None):
        if ContentGraph.__instance is not None:
            raise Exception("Only single graph created")
        
        self._graph_builder = StateGraph(ContentState)
        self.graph: CompiledStateGraph = None

        with open(prompt_file) as stream:
            self.prompt = yaml.safe_load(stream)

        self.hook_graph = HookGraph.get_instance(llm, self.prompt["PROMPT_HOOK"])
        self.hook_graph.graph_builder()
        
        with open(hook_file) as stream:
            self.hook_sample = yaml.safe_load(stream)

        self.intro_graph = IntroGraph.get_instance(llm, self.prompt["PROMPT_INTRO"])
        self.intro_graph.graph_builder()

        self.main_graph = MainGraph.get_instance(llm, self.prompt["PROMPT_MAIN"])
        self.main_graph.graph_builder()

        self.end_graph = EndGraph.get_instance(llm, self.prompt["PROMPT_END"])
        self.end_graph.graph_builder()
    
    @staticmethod
    def get_instance(llm = None, prompt_file = None, hook_file = None):
        with ContentGraph.__lock:
            if ContentGraph.__instance is None:
                ContentGraph.__instance = ContentGraph(llm, prompt_file, hook_file)
            
            return ContentGraph.__instance
        
    def graph_builder(self):
        self._graph_builder.add_node("content_generator", self.generate_content)
        self._graph_builder.add_edge(START, "content_generator")
        self._graph_builder.add_edge("content_generator", END)
        self.graph = self._graph_builder.compile()

    def generate_content(self, state: ContentState):
        hook_response = self.hook_graph.graph.stream({
            "structure": state["structure"],
            "description": state["description"],
            "hook_sample": state["hook_sample"]
            # "hook_sample": self.hook_sample["HOOK"]
        })
        hook_sentence = None
        for event in hook_response:
            for key, value, in event.items():
                if key == "hook":
                    hook_sentence = value
                    break

        intro_response = self.intro_graph.graph.stream({
           "style": state["style"],
           "structure": state["structure"], 
           "description": state["description"], 
           "hook": hook_sentence
        })
        intro = None
        for event in intro_response:
            for key, value, in event.items():
                if key == "intro":
                    intro = value
                    break

        
        main_response = self.main_graph.graph.stream({
           "structure": state["structure"], 
           "description": state["description"], 
           "hook": hook_sentence,
           "intro": intro
        })
        _main = None
        for event in main_response:
            for key, value, in event.items():
                if key == "main":
                    _main = value
                    break
                    
        end_response = self.end_graph.graph.stream({
           "structure": state["structure"], 
           "description": state["description"], 
           "hook": hook_sentence,
           "intro": intro,
           "main": _main
        })
        end = None
        for event in end_response:
            for key, value, in event.items():
                if key == "end":
                    end = value
                    break
        
        content = "Câu hook: " + hook_sentence + "\n\nPhần mở đầu: " + intro + "\n\nPhần thân: " + _main + "\n\nPhần cuối: " + end

        return {"content": content}
            
class HookGraph:
    __instance = None
    __lock = threading.Lock()

    def __init__(self, llm = None, prompt_hook = None):
        if HookGraph.__instance is not None:
            raise Exception("Only single graph created")
        
        self._graph_builder = StateGraph(HookState)
        self.graph: CompiledStateGraph = None
        self.llm: BaseChatModel = llm
        self.prompt_hook: str = prompt_hook

    @staticmethod
    def get_instance(llm = None, prompt_hook = None):
        with HookGraph.__lock:
            if HookGraph.__instance is None:
                HookGraph.__instance = HookGraph(llm, prompt_hook)
            
            return HookGraph.__instance
        
    def graph_builder(self):
        self._graph_builder.add_node("hook_generator", self.generate_hook)
        self._graph_builder.add_edge(START, "hook_generator")
        self._graph_builder.add_edge("hook_generator", END)
        self.graph = self._graph_builder.compile()

    def generate_hook(self, state: HookState):
        prompt = self.__instance.prompt_hook.format(state["structure"], state["description"], state["hook_sample"])
        hook_sentence = self.llm.invoke(prompt)
        return {"hook": hook_sentence.content}

class IntroGraph:
    __instance = None
    __lock = threading.Lock()

    def __init__(self, llm, prompt_intro):
        if IntroGraph.__instance is not None:
            raise Exception("Only single graph created")
        
        self._graph_builder = StateGraph(IntroState)
        self.graph: CompiledStateGraph = None
        self.llm: BaseChatModel = llm
        self.prompt_intro: str = prompt_intro
    
    @staticmethod
    def get_instance(llm, prompt_intro):
        with IntroGraph.__lock:
            if IntroGraph.__instance is None:
                IntroGraph.__instance = IntroGraph(llm, prompt_intro)
            
            return IntroGraph.__instance
        
    def graph_builder(self):
        self._graph_builder.add_node("intro_generator", self.generate_intro)
        self._graph_builder.add_edge(START, "intro_generator")
        self._graph_builder.add_edge("intro_generator", END)
        self.graph = self._graph_builder.compile()

    def generate_intro(self, state: IntroState):
        prompt = self.__instance.prompt_intro.format(
            state["style"], 
            state["structure"], 
            state["description"], 
            state["hook"]
        )

        intro = self.llm.invoke(prompt)
        return {"intro": intro.content}

class MainGraph:
    __instance = None
    __lock = threading.Lock()

    def __init__(self, llm, prompt_main):
        if MainGraph.__instance is not None:
            raise Exception("Only single graph created")
        
        self._graph_builder = StateGraph(IntroState)
        self.graph: CompiledStateGraph = None
        self.llm: BaseChatModel = llm
        self.prompt_main: str = prompt_main

    @staticmethod
    def get_instance(llm, prompt_main):
        with MainGraph.__lock:
            if MainGraph.__instance is None:
                MainGraph.__instance = MainGraph(llm, prompt_main)
            
            return MainGraph.__instance
        
    def graph_builder(self):
        self._graph_builder.add_node("main_generator", self.generate_main)
        self._graph_builder.add_edge(START, "main_generator")
        self._graph_builder.add_edge("main_generator", END)
        self.graph = self._graph_builder.compile()

    def generate_main(self, state: MainState):
        prompt = self.__instance.prompt_main.format(
            state["structure"],
            state["description"],
            state["hook"],
            state["intro"]
        )

        _main = self.llm.invoke(prompt)
        return {"main": _main.content}
        
class EndGraph:
    __instance = None
    __lock = threading.Lock()

    def __init__(self, llm, prompt_end):
        if EndGraph.__instance is not None:
            raise Exception("Only single graph created")
        
        self._graph_builder = StateGraph(EndState)
        self.graph: CompiledStateGraph = None
        self.llm: BaseChatModel = llm
        self.prompt_end: str = prompt_end

    @staticmethod
    def get_instance(llm, prompt_end):
        with EndGraph.__lock:
            if EndGraph.__instance is None:
                EndGraph.__instance = EndGraph(llm, prompt_end)
            
            return EndGraph.__instance
        
    def graph_builder(self):
        self._graph_builder.add_node("end_generator", self.generate_end)
        self._graph_builder.add_edge(START, "end_generator")
        self._graph_builder.add_edge("end_generator", END)
        self.graph = self._graph_builder.compile()

    def generate_end(self, state: EndState):
        prompt = self.__instance.prompt_end.format(
            state["structure"],
            state["description"],
            state["hook"],
            state["intro"],
            state["main"]
        )

        end = self.llm.invoke(prompt)
        return {"end": end.content}
    
class ModifierGraph:
    __instance = None
    __lock = threading.Lock()

    def __init__(self, llm, prompt_modifier_file):
        if ModifierGraph.__instance is not None:
            raise Exception("Only single graph created")
        
        self._graph_builder = StateGraph(ModifierState)
        self.graph: CompiledStateGraph = None
        self.llm: BaseChatModel = llm
        with open(prompt_modifier_file) as stream:
            self.prompt_modifier: str = yaml.safe_load(stream)["PROMPT_MODIFIER"]
        self.memory = MemorySaver()

    @staticmethod
    def get_instance(llm, prompt_modifier):
        with ModifierGraph.__lock:
            if ModifierGraph.__instance is None:
                ModifierGraph.__instance = ModifierGraph(llm, prompt_modifier)
            
            return ModifierGraph.__instance
        
    def graph_builder(self):
        self._graph_builder.add_node("content_modifier", self.modify_content)
        self._graph_builder.add_edge(START, "content_modifier")
        self._graph_builder.add_edge("content_modifier", END)
        self.graph = self._graph_builder.compile(checkpointer=self.memory)

    def modify_content(self, state: ModifierState):
        prompt = self.prompt_modifier.format(
            state['feedback'],
            state["content"]
        )

        modified_content = self.llm.invoke(prompt)
        return {"modified_content": modified_content.content}
    
class CheckerGraph:
    __instance = None
    __lock = threading.Lock()

    def __init__(self, llm, prompt_checker_file):
        if CheckerGraph.__instance is not None:
            raise Exception("Only single graph created")
        
        self._graph_builder = StateGraph(CheckerState)
        self.graph: CompiledStateGraph = None
        self.llm: BaseChatModel = llm
        with open(prompt_checker_file) as stream:
            data = yaml.safe_load(stream)
            self.prompt_checker: str = data["PROMPT_CHECKER"]
            self.policy = data["POLICY"]

    @staticmethod
    def get_instance(llm, prompt_checker):
        with CheckerGraph.__lock:
            if CheckerGraph.__instance is None:
                CheckerGraph.__instance = CheckerGraph(llm, prompt_checker)
            
            return CheckerGraph.__instance
        
    def graph_builder(self):
        self._graph_builder.add_node("content_checker", self.check_content)
        self._graph_builder.add_edge(START, "content_checker")
        self._graph_builder.add_edge("content_checker", END)
        self.graph = self._graph_builder.compile()

    def check_content(self, state: ModifierState):
        prompt = self.prompt_checker.format(
            state['content'],
            self.policy
        )

        modified_content = self.llm.invoke(prompt)
        return {"feedback": modified_content.content}