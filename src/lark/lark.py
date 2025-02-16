import lark_oapi as lark
import json

from lark_oapi.api.im.v1 import (
    P2ImMessageReceiveV1,
    CreateMessageRequest,
    CreateMessageRequestBody,
    ReplyMessageRequest,
    ReplyMessageRequestBody
)

from .client import SingletonLark
from src.utils import SingletonQueue
from src.llms import genenrate_content
from src.constants import CALL_OPENAI

resp_queue = SingletonQueue.get_instance()
client = SingletonLark.get_instance()

def create_request_thread(data: P2ImMessageReceiveV1, content: str) -> ReplyMessageRequest:
    request: ReplyMessageRequest = ReplyMessageRequest.builder() \
        .message_id(data.event.message.message_id) \
        .request_body(ReplyMessageRequestBody.builder()
            .content(content)
            .msg_type("text")
            .reply_in_thread(True)
            .build()) \
        .build()
    

    return request

def create_request_normal(data: P2ImMessageReceiveV1, content: str) -> CreateMessageRequest:
    request = CreateMessageRequest.builder() \
        .receive_id_type("chat_id") \
        .request_body(CreateMessageRequestBody.builder()
                        .receive_id(data.event.message.chat_id)
                        .msg_type("text")
                        .content(content)
                        .build()) \
        .build()
    
    return request

def send_request(data: P2ImMessageReceiveV1):
    msg = data.event.message
    # answer = call_openai(msg.content)
    # content = genenrate_content(description=msg.content)

    content = json.dumps({"text": "Answer in thread"})

    if data.event.message.thread_id is None:
        request = create_request_normal(data, content)
    else:
        request = create_request_thread(data, content)

    response = client.client.im.v1.chat.create(request) 
    if not response.success():
        raise Exception(
            f"client.im.v1.chat.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")



def do_p2_im_message_receive_v1(data: P2ImMessageReceiveV1):
    resp_queue.put((CALL_OPENAI, data, send_request))
    