import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message, send_image_url

load_dotenv()


machine = TocMachine(
    states=[
        "user",
        "helper",
        "body_graph",
        "fsm_graph",
        "where_sore",
        "back_sore",
        "shoulder_sore",
        "how_to_solve", 
        "appliance",
        "target_muscle",
        "tutorial",
        "recommend",
    ],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "helper",
            "conditions": "is_going_to_helper",
        },
        {
            "trigger": "advance",
            "source": "helper",
            "dest": "user",
            "conditions": "is_going_to_user",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "body_graph",
            "conditions": "is_going_to_body_graph",
        },
        {
            "trigger": "advance",
            "source": "body_graph",
            "dest": "user",
            "conditions": "is_going_to_user",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "fsm_graph",
            "conditions": "is_going_to_fsm_graph",
        },
        {
            "trigger": "advance",
            "source": "fsm_graph",
            "dest": "user",
            "conditions": "is_going_to_user",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "where_sore",
            "conditions": "is_going_to_where_sore",
        },
        {
            "trigger": "advance",
            "source": "where_sore",
            "dest": "user",
            "conditions": "is_going_to_user",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "back_sore",
            "conditions": "is_going_to_back_sore",
        },
        {
            "trigger": "advance",
            "source": "back_sore",
            "dest": "user",
            "conditions": "is_going_to_user",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "shoulder_sore",
            "conditions": "is_going_to_shoulder_sore",
        },
        {
            "trigger": "advance",
            "source": "shoulder_sore",
            "dest": "user",
            "conditions": "is_going_to_user",
        },
        {
            "trigger": "advance",
            "source": "where_sore",
            "dest": "back_sore",
            "conditions": "is_going_to_back_sore",
        },
        {
            "trigger": "advance",
            "source": "back_sore",
            "dest": "where_sore",
            "conditions": "is_going_to_where_sore",
        },
        {
            "trigger": "advance",
            "source": "where_sore",
            "dest": "shoulder_sore",
            "conditions": "is_going_to_shoulder_sore",
        },
        {
            "trigger": "advance",
            "source": "shoulder_sore",
            "dest": "where_sore",
            "conditions": "is_going_to_where_sore",
        },
        {
            "trigger": "advance",
            "source": "back_sore",
            "dest": "how_to_solve",
            "conditions": "is_going_to_how_to_solve",
        },
        {
            "trigger": "advance",
            "source": "shoulder_sore",
            "dest": "how_to_solve",
            "conditions": "is_going_to_how_to_solve",
        },
        {
            "trigger": "advance",
            "source": "how_to_solve",
            "dest": "user",
            "conditions": "is_going_to_user",
        },
        {
            "trigger": "advance",
            "source": "how_to_solve",
            "dest": "appliance",
            "conditions": "is_going_to_appliance",
        },
        {
            "trigger": "advance",
            "source": "appliance",
            "dest": "how_to_solve",
            "conditions": "is_going_to_how_to_solve",
        },
        {
            "trigger": "advance",
            "source": "appliance",
            "dest": "user",
            "conditions": "is_going_to_user",
        },
        {
            "trigger": "advance",
            "source": "how_to_solve",
            "dest": "target_muscle",
            "conditions": "is_going_to_target_muscle",
        },
        {
            "trigger": "advance",
            "source": "target_muscle",
            "dest": "how_to_solve",
            "conditions": "is_going_to_how_to_solve",
        },
        {
            "trigger": "advance",
            "source": "target_muscle",
            "dest": "user",
            "conditions": "is_going_to_user",
        },
        {
            "trigger": "advance",
            "source": "how_to_solve",
            "dest": "tutorial",
            "conditions": "is_going_to_tutorial",
        },
        {
            "trigger": "advance",
            "source": "tutorial",
            "dest": "how_to_solve",
            "conditions": "is_going_to_how_to_solve",
        },
        {
            "trigger": "advance",
            "source": "tutorial",
            "dest": "user",
            "conditions": "is_going_to_user",
        },
        {
            "trigger": "advance",
            "source": "how_to_solve",
            "dest": "recommend",
            "conditions": "is_going_to_recommend",
        },
        {
            "trigger": "advance",
            "source": "recommend",
            "dest": "how_to_solve",
            "conditions": "is_going_to_how_to_solve",
        },
        {
            "trigger": "advance",
            "source": "recommend",
            "dest": "user",
            "conditions": "is_going_to_user",
        },
        {
            "trigger": "advance",
            "source": [
                "helper",
                "fsm_graph",
                "where_sore",
                "back_sore",
                "shoulder_sore",
                "how_to_solve",
                "appliance",
                "target_muscle",
                "tutorial",
                "recommend",
            ],
            "dest": "body_graph",
            "conditions": "is_going_to_body_graph",
        },
        {
            "trigger": "advance",
            "source": "body_graph",
            "dest": "helper",
            "conditions": "is_going_to_helper",
        },
        {
            "trigger": "advance",
            "source": "body_graph",
            "dest": "fsm_graph",
            "conditions": "is_going_to_fsm_graph",
        },
        {
            "trigger": "advance",
            "source": "body_graph",
            "dest": "where_sore",
            "conditions": "is_going_to_where_sore",
        },
        {
            "trigger": "advance",
            "source": "body_graph",
            "dest": "back_sore",
            "conditions": "is_going_to_back_sore",
        },
        {
            "trigger": "advance",
            "source": "body_graph",
            "dest": "shoulder_sore",
            "conditions": "is_going_to_shoulder_sore",
        },
        {
            "trigger": "advance",
            "source": "body_graph",
            "dest": "how_to_solve",
            "conditions": "is_going_to_how_to_solve",
        },
        {
            "trigger": "advance",
            "source": "body_graph",
            "dest": "appliance",
            "conditions": "is_going_to_appliance",
        },
        {
            "trigger": "advance",
            "source": "body_graph",
            "dest": "target_muscle",
            "conditions": "is_going_to_target_muscle",
        },
        {
            "trigger": "advance",
            "source": "body_graph",
            "dest": "tutorial",
            "conditions": "is_going_to_tutorial",
        },
        {
            "trigger": "advance",
            "source": "body_graph",
            "dest": "recommend",
            "conditions": "is_going_to_recommend",
        },
        {
            "trigger": "go_back",
            "source": [
                "helper",
                "body_graph",
                "fsm_graph",
                "where_sore",
                "back_sore",
                "shoulder_sore",
                "how_to_solve",
                "appliance",
                "target_muscle",
                "tutorial",
                "recommend",
            ],
            "dest": "user"
        },
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", "cf197afa8f13720c856345552a8cb63e")
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "4Vmuh1fBve0HDaj1/1BsxCdedVtwV5TMgY6KVQUt4g8V75GwftAt8NzC3PHT+xULn5BADYODpMj7XD5dP9nd603dfGtir8egUAJCJnG+jBxMx1Jiw7sClpiif/wZT8b3pdXnv+JbWKGqOsDq2vFM3AdB04t89/1O/w1cDnyilFU=")
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")

        # get response from machine
        response = machine.advance(event)

        # exception
        if response == False:
            if machine.state == 'user':
                # show the message which user may want to know
                user_msg = '歡迎使用肌肉痠痛小幫手~\n' \
                           '若輸入關節字則會啟動特殊功能\n'\
                           '輸入 "help" 會說明所有關鍵字\n'
                send_text_message(event.reply_token, user_msg)
            
            if machine.state == 'shoulder_sore' or machine.state == 'back_sore':
                # show the message which user may want to know
                user_msg = '請輸入 "如何放鬆"\n' \
                           '來了解放鬆的方式\n'
                send_text_message(event.reply_token, user_msg)

            else:
                # show the message which user may want to know
                user_msg = '如果想回到上一個狀態\n' \
                           '請輸入 "back"\n\n' \
                           '如果輸入 "back"\n' \
                           '依然跳出此訊息\n' \
                           '請勇敢輸入 "restart"\n\n' \
                           '如果想回到最初的狀態\n' \
                           '請輸入 "restart"\n' 
                send_text_message(event.reply_token, user_msg)

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
