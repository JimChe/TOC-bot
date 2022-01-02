from transitions.extensions import GraphMachine

from utils import send_text_message, send_image_url


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_user(self, event):
        text = event.message.text
        return text.lower() == 'back'

    def is_going_to_helper(self, event):
        text = event.message.text
        return text.lower() == 'help'
    
    def is_going_to_body_graph(self, event):
        text = event.message.text
        return text.lower() == '人體肌肉圖'

    def is_going_to_fsm_graph(self, event):
        text = event.message.text
        return text.lower() == 'fsm'

    def is_going_to_where_sore(self, event):
        text = event.message.text
        return text.lower() == '痠痛'

    def is_going_to_back_sore(self, event):
        text = event.message.text
        return text.lower() == '背部痠痛'

    def is_going_to_shoulder_sore(self, event):
        text = event.message.text
        return text.lower() == '肩頸痠痛'

    def on_enter_user(self, event):
        # show the message which user may want to know
        user_msg = '歡迎使用肌肉痠痛小幫手~\n' \
                    '若輸入關節字則會啟動特殊功能\n'\
                    '輸入 "help" 會說明所有關鍵字\n'
        send_text_message(event.reply_token, user_msg)

    def on_enter_helper(self, event):
        # if enter help
        if event.message.text.lower() == 'help':
            help_msg = '"痠痛": 小幫手會詢問酸痛的部位\n\n' \
                        '"肩頸痠痛 或 背部痠痛": 小幫手會跳出相關舒緩方式\n\n' \
                        '"人體肌肉圖": 跳出人體肌肉分布圖片\n'
            send_text_message(event.reply_token, help_msg)

    def on_enter_body_graph(self, event):
        # if enter 'Human anatomy diagram'
        if event.message.text.lower() == '人體肌肉圖':
            img_url = 'https://i.imgur.com/hlOZpVf.jpg'
            send_image_url(event.reply_token, img_url)

    def on_enter_fsm_graph(self, event):
        # if enter fsm
        if event.message.text.lower() == 'fsm':
            send_image_url(event.reply_token, 'https://muscle-sore-line-bot.herokuapp.com/show-fsm')
    
    def on_enter_where_sore(self, event):
        sore_msg = '請問是哪個地方痠痛呢?\n' \
                    '"肩頸痠痛" 還是 "背部痠痛"?\n' \
                    '請輸入兩者之一觀看舒緩方法\n'
        send_text_message(event.reply_token, sore_msg)

    def on_enter_back_sore(self, event):
        sore_msg = '建議放鬆部位:\n' \
                    '豎脊肌\n' \
                    '背闊肌\n' \
                    '大圓肌\n' \
                    '小圓肌\n' \
                    '中下斜方肌\n' 
        send_text_message(event.reply_token, sore_msg)

    def on_enter_shoulder_sore(self, event):
        sore_msg = '建議放鬆部位:\n' \
                    '上斜方肌\n' \
                    '提肩胛肌\n'
        send_text_message(event.reply_token, sore_msg)
