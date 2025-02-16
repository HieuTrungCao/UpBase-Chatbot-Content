
import os
import json
import threading

from flask import Flask
from lark_oapi.adapter.flask import parse_req, parse_resp
from lark_oapi import EventDispatcherHandler, LogLevel
from dotenv import load_dotenv

from src.lark import do_p2_im_message_receive_v1
from src.utils import call_llm

load_dotenv()

ENCRYPT_KEY = os.getenv("ENCRYPT_KEY")
VERIFICATION_TOKEN = os.getenv("VERIFICATION_TOKEN")

app = Flask("Customer Supporter")

event_handler = EventDispatcherHandler.builder(ENCRYPT_KEY, VERIFICATION_TOKEN, LogLevel.DEBUG)\
    .register_p2_im_message_receive_v1(do_p2_im_message_receive_v1)\
    .build()
            

thread = threading.Thread(target=call_llm, daemon=True) # daemon=True important
thread.start()


@app.route("/event", methods=["POST"])
def event():
    resp = event_handler.do(parse_req())
    return parse_resp(resp)

app.run(port=3000, debug=True)


description = '''
Viên uống Esunvy giúp giảm thâm nám trên da, giảm tình trạng mụn, phục hồi vùng da bị tổn thương. Đồng thời, sản phẩm còn có tác dụng với chức năng gan, giúp thanh nhiệt, giải độc gan
Ưu điểm nổi bật:
    Nguyên liệu có nguồn gốc tự nhiên, an toàn với người dùng
    Được chứng minh tính hiệu quả trên tất cả các loại mụn
    Sản xuất bởi Công ty Cổ phần Dược phẩm Gia Nguyễn đạt tiêu chuẩn thực hành sản xuất tốt GMP-WHO, được Cục An toàn thực phẩm cấp giấy chứng nhận
'''