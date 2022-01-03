from transitions.extensions import GraphMachine

from linebot.models import MessageTemplateAction, ImageCarouselColumn, URITemplateAction

from utils import send_text_message, send_image_url, send_button_message, send_carousel_message

#from bs4 import BeautifulSoup
import requests

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.sore = 0
        self.pre_state = 'user'
        self.cur_state = 'user'
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_user(self, event):
        text = event.message.text
        return text.lower() == 'restart' \
            or (self.cur_state == 'helper'     and text.lower() == 'back') \
            or (self.cur_state == 'fsm_graph'  and text.lower() == 'back') \
            or (self.cur_state == 'body_graph' and text.lower() == 'back')

    def is_going_to_helper(self, event):
        text = event.message.text
        return text.lower() == 'help' \
            or (self.cur_state == 'body_graph' and text.lower() == 'back')
    
    def is_going_to_body_graph(self, event):
        text = event.message.text
        return text.lower() == '人體肌肉圖'

    def is_going_to_fsm_graph(self, event):
        text = event.message.text
        return text.lower() == 'fsm' \
            or (self.cur_state == 'body_graph' and text.lower() == 'back')

    def is_going_to_where_sore(self, event):
        text = event.message.text
        return text.lower() == '痠痛' \
            or (self.cur_state == 'body_graph' and text.lower() == 'back') \
            or (self.cur_state == 'back_sore' and text.lower() == 'back') \
            or (self.cur_state == 'shoulder_sore' and text.lower() == 'back')

    def is_going_to_back_sore(self, event):
        text = event.message.text
        return text.lower() == '背部痠痛' \
            or (self.cur_state == 'body_graph' and text.lower() == 'back')

    def is_going_to_shoulder_sore(self, event):
        text = event.message.text
        return text.lower() == '肩頸痠痛' \
            or (self.cur_state == 'body_graph' and text.lower() == 'back')

    def is_going_to_how_to_solve(self, event):
        text = event.message.text
        return text.lower() == '如何放鬆' \
            or (self.cur_state == 'body_graph' and text.lower() == 'back')
    
    def is_going_to_appliance(self, event):
        text = event.message.text
        return text.lower() == '放鬆用具' \
            or (self.cur_state == 'body_graph' and text.lower() == 'back')

    def is_going_to_target_muscle(self, event):
        text = event.message.text
        return text.lower() == '放鬆位置'\
            or (self.cur_state == 'body_graph' and text.lower() == 'back')

    def is_going_to_tutorial(self, event):
        text = event.message.text
        return text.lower() == '教學'\
            or (self.cur_state == 'body_graph' and text.lower() == 'back')

    def is_going_to_recommend(self, event):
        text = event.message.text
        return text.lower() == '還是不懂'\
            or (self.cur_state == 'body_graph' and text.lower() == 'back')


    def on_enter_user(self, event):
        self.pre_state = self.cur_state
        self.cur_state = 'user'
        # show the message which user may want to know
        msg = '歡迎使用肌肉痠痛小幫手~\n' \
                    '若輸入關節字則會啟動特殊功能\n'\
                    '輸入 "help" 會說明所有關鍵字\n'
        send_text_message(event.reply_token, msg)

    def on_enter_helper(self, event):
        self.pre_state = self.cur_state
        self.cur_state = 'helper'
        # enter help
        msg = '"痠痛": 小幫手會詢問酸痛的部位\n\n' \
                    '"肩頸痠痛 或 背部痠痛": 小幫手會跳出相關舒緩方式\n\n' \
                    '"人體肌肉圖": 跳出人體肌肉分布圖片\n' \
                    '*"人體肌肉圖" 在任何狀態都可以輸入\n'
        send_text_message(event.reply_token, msg)

    def on_enter_body_graph(self, event):
        self.pre_state = self.cur_state
        self.cur_state = 'body_graph'
        # if enter 'Human anatomy diagram'
        img_url = 'https://i.imgur.com/hlOZpVf.jpg'
        send_image_url(event.reply_token, img_url)

    def on_enter_fsm_graph(self, event):
        self.pre_state = self.cur_state
        self.cur_state = 'fsm_graph'
        # if enter fsm
        send_image_url(event.reply_token, 'https://muscle-sore-line-bot.herokuapp.com/show-fsm')
    
    def on_enter_where_sore(self, event):
        self.pre_state = self.cur_state
        self.cur_state = 'where_sore'
        msg = '請問是哪個地方痠痛呢?\n' \
                    '"肩頸痠痛" 還是 "背部痠痛"?\n' \
                    '請輸入兩者之一觀看舒緩方法\n'
        send_text_message(event.reply_token, msg)

    def on_enter_back_sore(self, event):
        self.pre_state = self.cur_state
        self.cur_state = 'back_sore'
        self.sore = 0
        msg = '建議放鬆部位:\n' \
                    '豎脊肌\n' \
                    '背闊肌\n' \
                    '大圓肌\n' \
                    '小圓肌\n' \
                    '中下斜方肌\n' \
                    '可以輸入 "如何放鬆"\n' \
                    '了解更多放鬆細節'
        send_text_message(event.reply_token, msg)

    def on_enter_shoulder_sore(self, event):
        self.pre_state = self.cur_state
        self.cur_state = 'shoulder_sore'
        self.sore = 1
        msg = '建議放鬆部位:\n' \
                    '上斜方肌\n' \
                    '提肩胛肌\n' \
                    '可以輸入 "如何放鬆"\n' \
                    '了解更多放鬆細節'
        send_text_message(event.reply_token, msg)

    def on_enter_how_to_solve(self, event):
        self.pre_state = self.cur_state
        title = ''
        url = ''
        if self.sore == 0:
            title = '舒緩背部痠痛相關事項說明'
            url = 'https://www.dongrens.com/wp-content/uploads/2020/12/1029671.jpg'
        else:
            title = '舒緩肩頸痠痛相關事項說明'
            url = 'https://fastzonemassage.com/wp-content/uploads/2019/05/1.jpg'
        
        self.cur_state = 'how_to_solve'
        text = '請選擇『放鬆用具』或『放鬆位置』或『教學』'
        btn = [
            MessageTemplateAction(
                label='放鬆用具',
                text='放鬆用具'
            ),
            MessageTemplateAction(
                label='放鬆位置',
                text='放鬆位置'
            ),
            MessageTemplateAction(
                label='教學',
                text='教學'
            ),
        ]
        send_button_message(event.reply_token, title, text, btn, url)

    def on_enter_appliance(self, event):
        self.pre_state = self.cur_state
        self.cur_state = 'appliance'
        # if enter fsm
        send_image_url(event.reply_token, 'https://cf.shopee.tw/file/c31ed7c9d4b4d1bb32cc8ae2229363f9')

    def on_enter_target_muscle(self, event):
        if self.sore == 0:
            img_url = 'https://s3-ap-northeast-1.amazonaws.com/upload.potatomedia.co/articles/potato_36fe9a10-3536-487e-96fa-fa2373271653_ceeceae875b6f0f5151801d78d259d9d959cd4df.png'
        else:
            img_url = 'https://blog.easepain.tw/wp-content/uploads/2018/10/%E8%82%A9%E8%83%9B%E9%AA%A8%E7%9A%84%E8%82%8C%E8%82%89%EF%BC%8C%E4%B8%8A%E6%96%9C%E6%96%B9%E8%82%8C%E4%B8%AD%E6%96%9C%E6%96%B9%E8%82%8C%E8%8F%B1%E5%BD%A2%E8%82%8C.jpg'

        self.pre_state = self.cur_state
        self.cur_state = 'target_muscle'
        # if enter fsm
        send_image_url(event.reply_token, img_url)

    def on_enter_tutorial(self, event):
        self.pre_state = self.cur_state
        self.cur_state = 'tutorial'
        msg = '放鬆教學:\n' \
                '1. 將按摩球對準目標肌肉的位置\n' \
                '2. 靠牆或躺下\n' \
                '3. 利用體重作為施力來源按壓\n' \
                '4. 按壓過程慢慢移動位置\n' \
                '5. 尋找到痠痛的點時停下\n' \
                '6. 在酸痛點來回移動或是靜止\n' \
                '7. 重複4.~6.直到按壓完整塊肌肉\n'
        send_text_message(event.reply_token, msg)

    def on_enter_recommend(self, event):
        self.pre_state = self.cur_state
        self.cur_state = 'recommend'
        msg = '由於技術問題\n' \
                '更加詳細的內容\n' \
                '小幫手無法提供了啦\n' \
                '推薦觀看youtube上\n' \
                '物理治療師的相關影片\n' \
                '"sun guts" 是其中一位\n' \
                '影片內容清楚易懂的yt\n' \
                '想了解更多\n' \
                'google也有非常多參考文章哦\n'
        send_text_message(event.reply_token, msg)
