from linebot import LineBotApi
from linebot.models import TextSendMessage,TemplateSendMessage,ConfirmTemplate,MessageAction
from linebot.exceptions import LineBotApiError

import schedule
import time

import json
with open('../../lineapi.json') as line:
    line_api_json = json.load(line)
ACCESSTOKEN = line_api_json['ACCESSTOKEN']
USERID = line_api_json['USERID']

line_bot_api = LineBotApi(ACCESSTOKEN)

def main():
  confirm_template_message1 = TemplateSendMessage(
                                alt_text='Confirm template',
                                template=ConfirmTemplate(
                                    text='1つ目の目薬を打ちましたか？',
                                    actions=[
                                        MessageAction(
                                            label='はい',
                                            text='はい',
                                        ),
                                        MessageAction(
                                            label='いいえ',
                                            text='いいえ'
                                        )
                                    ]
                                )
                            )
  try:
    line_bot_api.push_message(USERID, confirm_template_message1)
  except LineBotApiError as e:
      pass

if __name__ == "__main__":
  main()