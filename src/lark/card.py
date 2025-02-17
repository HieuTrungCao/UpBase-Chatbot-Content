import json
import lark_oapi as lark

from lark_oapi.api.im.v1 import(
    CreateMessageRequest,
    CreateMessageRequestBody,
    P2ImMessageReceiveV1
)

from .client import SingletonLark

card_config = json.load(open("card/card.json"))

client = SingletonLark.get_instance()

def create_card(data: P2ImMessageReceiveV1) -> None:
    request = CreateMessageRequest.builder() \
        .receive_id_type("chat_id") \
        .request_body(CreateMessageRequestBody.builder()
                      .receive_id(data.event.message.chat_id)
                      .msg_type("interactive")
                      .content(lark.JSON.marshal(card_config))
                      .build()) \
        .build()
    
    response = client.client.im.v1.chat.create(request)
    
    if not response.success():
        raise Exception(
            f"client.im.v1.chat.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")