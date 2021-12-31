from linebot import LineBotApi
from linebot.models import TemplateSendMessage,ConfirmTemplate,MessageAction
from linebot.exceptions import LineBotApiError

#import sys
#sys.path.append('../eye_drops/')
#import libraries

import os
import json

ACCESSTOKEN = os.environ.get("ACCESSTOKEN")
USERID = os.environ.get("USERID")
line_bot_api = LineBotApi(ACCESSTOKEN)

def main():
  
  confirm_template_message1 = TemplateSendMessage(
                                alt_text='目薬の時間です',
                                template=ConfirmTemplate(
                                    text='1つ目の目薬を打ちましたか？',
                                    actions=[
                                        MessageAction(
                                            label='はい',
                                            text='はい'
                                        ),
                                        MessageAction(
                                            label='いいえ',
                                            text='いいえ'
                                        )
                                    ]
                                )
                            )

  #confirm_template_message1 = libraries.push_message(1)
  
  try:
    line_bot_api.push_message(USERID, messages=confirm_template_message1)
  except LineBotApiError as e:
    pass

if __name__ == "__main__":
  main()