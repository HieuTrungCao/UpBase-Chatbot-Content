from lark_oapi.api.im.v1 import (
    P2ImMessageReceiveV1,
    CreateMessageRequest,
    CreateMessageRequestBody
)

from .client import SingletonLark
from src.utils import SingletonQueue
from src.llms import genenrate_conten
from src.constants import CALL_OPENAI

resp_queue = SingletonQueue.get_instance()
client = SingletonLark.get_instance()

def send_request(data: P2ImMessageReceiveV1):
    msg = data.event.message
    # answer = call_openai(msg.content)
    content = genenrate_conten(description=msg.content)

    request = CreateMessageRequest.builder() \
        .receive_id_type("chat_id") \
        .request_body(CreateMessageRequestBody.builder()
                        .receive_id(msg.chat_id)
                        .msg_type("text")
                        .content(content)
                        .build()) \
        .build()

    response = client.client.im.v1.chat.create(request) 
    if not response.success():
        raise Exception(
            f"client.im.v1.chat.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")



def do_p2_im_message_receive_v1(data: P2ImMessageReceiveV1):
    resp_queue.put((CALL_OPENAI, data, send_request))
    