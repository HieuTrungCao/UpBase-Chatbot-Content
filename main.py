
import os
import json
import threading

from flask import Flask
from lark_oapi.adapter.flask import parse_req, parse_resp
from lark_oapi import EventDispatcherHandler, LogLevel
from dotenv import load_dotenv

from src.lark.lib.action_handler import CardActionHandler
from src.lark import do_p2_im_message_receive_v1, do_interactive_card
from src.utils import call_llm

load_dotenv()

ENCRYPT_KEY = os.getenv("ENCRYPT_KEY")
VERIFICATION_TOKEN = os.getenv("VERIFICATION_TOKEN")

app = Flask("Content Generator")

event_handler = EventDispatcherHandler.builder(ENCRYPT_KEY, VERIFICATION_TOKEN, LogLevel.DEBUG)\
    .register_p2_im_message_receive_v1(do_p2_im_message_receive_v1)\
    .build()
            

card_handler = CardActionHandler.builder(ENCRYPT_KEY, VERIFICATION_TOKEN, LogLevel.DEBUG) \
    .register(do_interactive_card) \
    .build()

thread = threading.Thread(target=call_llm, daemon=True) # daemon=True important
thread.start()


@app.route("/event", methods=["POST"])
def event():
    resp = event_handler.do(parse_req())
    return parse_resp(resp)

@app.route("/card", methods=["POST"])
def card():
    resp = card_handler.do(parse_req())
    return parse_resp(resp)

@app.route("/", methods=["GET"])
def home():
    return {"Status": "Connected!!"}

app.run(port=3000)