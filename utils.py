import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, \
TextMessage, TextSendMessage, ImageSendMessage, \
TemplateSendMessage, ButtonsTemplate, ImageCarouselTemplate


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "4Vmuh1fBve0HDaj1/1BsxCdedVtwV5TMgY6KVQUt4g8V75GwftAt8NzC3PHT+xULn5BADYODpMj7XD5dP9nd603dfGtir8egUAJCJnG+jBxMx1Jiw7sClpiif/wZT8b3pdXnv+JbWKGqOsDq2vFM3AdB04t89/1O/w1cDnyilFU=")

line_bot_api = LineBotApi(channel_access_token)

def send_text_message(reply_token, text):
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"


def send_image_url(reply_token, img_url):
    message = ImageSendMessage(
        original_content_url = img_url,
        preview_image_url = img_url
    )
    line_bot_api.reply_message(reply_token, message)
    
    return "OK"

def send_button_message(reply_token, title, text, btn, url):
    message = TemplateSendMessage(
        alt_text='button template',
        template = ButtonsTemplate(
            title = title,
            text = text,
            thumbnail_image_url = url,
            actions = btn
        )
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"


def send_carousel_message(reply_token, col):
    message = TemplateSendMessage(
        alt_text = 'Carousel template',
        template = ImageCarouselTemplate(columns = col)
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"
