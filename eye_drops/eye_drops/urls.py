"""eye_drops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

import json
with open('../lineapi.json') as line:
    line_api_json = json.load(line)
ACCESSTOKEN = line_api_json['ACCESSTOKEN']

from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi
from linebot.models import TextSendMessage,TemplateSendMessage,ConfirmTemplate,MessageAction
from linebot.exceptions import LineBotApiError


@csrf_exempt
def callback(request):
    sent_json = json.loads(request.body)
    text = sent_json['events'][0]['message']['text']
    reply_token = sent_json['events'][0]['replyToken']
    line_bot_api = LineBotApi(ACCESSTOKEN)
    
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
    
    confirm_template_message2 = TemplateSendMessage(
                                alt_text='Confirm template',
                                template=ConfirmTemplate(
                                    text='2つ目の目薬を打ちましたか？',
                                    actions=[
                                        MessageAction(
                                            label='完了しました',  #LINEの画面で表示される言葉
                                            text='完了しました',  #LINEからbotに送られる言葉
                                        ),
                                        MessageAction(
                                            label='まだです',
                                            text='まだです'
                                        )
                                    ]
                                )
                            )
    
    try:
        if text == "はい":
            line_bot_api.reply_message(reply_token, [TextSendMessage(text='お疲れさまです\n2つ目も忘れずに打ちましょう'), confirm_template_message2])
        elif text == "いいえ":
            line_bot_api.reply_message(reply_token, confirm_template_message1)
        elif text == "完了しました":
            line_bot_api.reply_message(reply_token, TextSendMessage(text='お疲れさまです\n次の時間も忘れずに打ちましょう'))
        elif text == "まだです":
            line_bot_api.reply_message(reply_token, confirm_template_message2)
        else:
            line_bot_api.reply_message(reply_token, confirm_template_message1)
    except LineBotApiError as e:
        pass

urlpatterns = [
    path('admin/', admin.site.urls),
    path('callback/', callback)
]
