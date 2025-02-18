from typing import Dict, Optional, Any, List

from lark_oapi.core.construct import init
from lark_oapi.core.model import RawRequest


class Header(object):
    _type = {}

    def __init__(self, d=None) -> None:
        self.event_id: Optional[str] = None
        self.token: Optional[str] = None
        self.create_time: Optional[str] = None
        self.event_type: Optional[str] = None
        self.tenant_key: Optional[str] = None
        self.app_id: Optional[str] = None
        init(self, d, self._type)

class Operator(object):
    _type = {}

    def __init__(self, d=None):
        self.tenant_key: Optional[str] = None
        self.open_id: Optional[str] = None
        self.union_id: Optional[str] = None
        init(self, d, self._type)

class Action(object):
    _types = {}

    def __init__(self, d=None) -> None:
        self.value: Dict[str, Any] = {}
        self.tag: Optional[str] = None
        self.option: Optional[str] = None
        self.timezone: Optional[str] = None
        self.name: Optional[str] = None
        self.form_value: Dict[str, Any] = {}
        self.input_value: Optional[str] = None
        self.options: Optional[List[str]] = []
        self.checked: Optional[bool] = None
        init(self, d, self._types)

class Context(object):
    _type = {}

    def __init__(self, d=None):
        self.open_message_id: Optional[str] = None
        self.open_chat_id: Optional[str] = None
        init(self, d, self._type)

class Event(object):
    _type = {
        "operator": Operator,
        "action": Action,
        "context": Context
    }

    def __init__(self, d=None):
        self.operator: Optional[Operator] = None
        self.token: Optional[str] = None
        self.action: Optional[Action] = None
        self.host: Optional[str] = None
        self.context: Optional[Context] = None
        init(self, d, self._type)
    
class Card(object):
    _types = {
        "header": Header,
        "event": Event
    }

    def __init__(self, d=None) -> None:
        self.schema: Optional[str] = None
        self.header: Optional[Header] = None
        self.event: Optional[Event] = None
        self.open_id: Optional[str] = None
        self.user_id: Optional[str] = None
        self.tenant_key: Optional[str] = None
        self.open_message_id: Optional[str] = None
        self.open_chat_id: Optional[str] = None
        self.token: Optional[str] = None
        self.challenge: Optional[str] = None
        self.type: Optional[str] = None
        self.action: Optional[Action] = None
        self.raw: Optional[RawRequest] = None
        init(self, d, self._types)