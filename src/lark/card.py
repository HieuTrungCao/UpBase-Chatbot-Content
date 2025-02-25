import json
import lark_oapi as lark
import os

from lark_oapi.api.im.v1 import(
    CreateMessageRequest,
    CreateMessageRequestBody,
    P2ImMessageReceiveV1,
    ReplyMessageRequest,
    ReplyMessageRequestBody
)

from .client import SingletonLark
from src.utils import SingletonQueue
from .lib.model import Card
from src.constants import (
    CREATE_THREAD
)
from src.postgres import Connector
from src.bot import Bot
from src.utils import get_structure, get_style, ContentList

card_config = json.load(open("card/card.json"))
policy_config = json.load(open("card/policy.json"))

client = SingletonLark.get_instance()
resp_queue = SingletonQueue.get_instance()
connector = Connector.get_instance()
bot = Bot.get_instance()
contents = ContentList.get_instance()

def create_request_thread(data: Card, content: str) -> ReplyMessageRequest:
    request: ReplyMessageRequest = ReplyMessageRequest.builder() \
        .message_id(data.event.context.open_message_id) \
        .request_body(ReplyMessageRequestBody.builder()
            .content(content)
            .msg_type("text")
            .reply_in_thread(True)
            .build()) \
        .build()

    return request
    
def create_card(data: P2ImMessageReceiveV1, is_create_content = True) -> None:
    if is_create_content:
        _card_config = card_config
    else: 
        _card_config = policy_config

    request = CreateMessageRequest.builder() \
        .receive_id_type("chat_id") \
        .request_body(CreateMessageRequestBody.builder()
                      .receive_id(data.event.message.chat_id)
                      .msg_type("interactive")
                      .content(lark.JSON.marshal(_card_config))
                      .build()) \
        .build()
    
    response = client.client.im.v1.chat.create(request)

    if not response.success():
        raise Exception(
            f"client.im.v1.chat.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")

def check_policy(data: Card):
    feedback = bot.check_policy(
        content=data.event.action.form_value["content"]
    )

    content = json.dumps({"text": feedback})

    request = create_request_thread(data, content)
    response = client.client.im.v1.chat.create(request) 

    if not response.success():
        raise Exception(
            f"client.im.v1.chat.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}"  
        )

def create_first_content(data: Card):

    card_id = data.event.context.open_message_id
    user_id = data.event.operator.union_id
    hook_sentence = data.event.action.form_value["hook_sentence"]
    description = data.event.action.form_value["description"]
    create_time = data.header.create_time

    content = bot.generate_content(
        structure=get_structure(),
        style=get_style(),
        description=description,
        hook=hook_sentence
    )

    contents.put_content(content)
    content = json.dumps({"text": content})

    request = create_request_thread(data, content)
    response = client.client.im.v1.chat.create(request) 
    resp = json.loads(response.raw.content)
    thread_id = resp["data"]["thread_id"]
    connector.insert_content((card_id, user_id, hook_sentence, description, thread_id, create_time))
    if not response.success():
        raise Exception(
            f"client.im.v1.chat.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}"  
        )

def save_user_id(data: Card):
    database_dir = "database"
    if not os.path.exists(database_dir):
        os.mkdir(database_dir)

    usage_file = os.path.join(database_dir, "usage.txt")

    user_id = data.event.operator.union_id

    try:
        with open(usage_file, "a") as usage_file_obj:
            usage_file_obj.write(user_id + "\n")
            usage_file_obj.close()
    except Exception as e:
        print(f"An error occurred: {e}")

def save_hook_sentence(data: Card):
    database_dir = "database"
    if not os.path.exists(database_dir):
        os.mkdir(database_dir)

    hook_file = os.path.join(database_dir, "hook.txt")

    hook = data.event.action.form_value["hook_sentence"]

    try:
        with open(hook_file, "a") as hook_file_obj:
            hook_file_obj.write(hook + "\n")
            hook_file_obj.close()
    except Exception as e:
        print(f"An error occurred: {e}")
    

def do_interactive_card(data: Card):
    if data.event is not None and data.event.action.name == "create":
        resp_queue.put((CREATE_THREAD, data, create_first_content))
        resp_queue.put((CREATE_THREAD, data, save_user_id))
        resp_queue.put((CREATE_THREAD, data, save_hook_sentence))
        return card_config

    if data.event is not None and data.event.action.name == "check":
        resp_queue.put((CREATE_THREAD, data, check_policy))
        return card_config
    
    return card_config