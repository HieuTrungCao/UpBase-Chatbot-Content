from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from typing import Annotated

class ContentState(TypedDict):
    structure: str
    style: str
    description: str
    hook_sample: str
    content: str

class HookState(TypedDict):
    hook: str
    description: str
    hook_sample: str
    structure: str

class IntroState(TypedDict):
    style: str
    structure: str
    description: str
    hook: str
    intro: str

class MainState(TypedDict):
    structure: str
    description: str
    hook: str
    intro: str
    main: str

class EndState(TypedDict):
    structure: str
    description: str
    hook: str
    intro: str
    main: str
    end: str

class ModifierState(TypedDict):
    content: str
    feedback: str
    modified_content: str