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

import sys
#from eye_drops.notification_bot.push_message import ACCESSTOKEN
sys.path.append('../')
import libraries

import json
import os
import time
import datetime
import schedule

from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi
from linebot.models import TextSendMessage,TemplateSendMessage,ConfirmTemplate,MessageAction
from linebot.exceptions import LineBotApiError

"""
file = open('../lineapi.json', 'r')
info = json.load(file)
ACCESSTOKEN = info['ACCESSTOKEN']
USERID = info['USERID']
line_bot_api = LineBotApi(ACCESSTOKEN)
"""
line_bot_api = LineBotApi(os.environ['ACCESSTOKEN'])
USERID = os.environ['USERID']

confirm_template_message1 = libraries.push_message(1, "はい", "いいえ")
confirm_template_message2 = libraries.push_message(2, "完了しました", "まだです")

@csrf_exempt
def callback(request):
    sent_json = json.loads(request.body)
    timestamp = sent_json['events'][0]['timestamp']
    timestamp = datetime.datetime.fromtimestamp(timestamp/1000)
    hour = timestamp.hour
    minutes = timestamp.minute
    text = sent_json['events'][0]['message']['text']
    reply_token = sent_json['events'][0]['replyToken']
    
    try:
        if text == "はい":
            line_bot_api.reply_message(reply_token, TextSendMessage(text='お疲れさまです\n5分後に2つ目の目薬の通知をします'))
            timer(hour,minutes)
            #line_bot_api.push_message(USERID, messages=confirm_template_message2)
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

def second_push_message():
    line_bot_api.push_message(USERID, messages=confirm_template_message2)

def timer(hour,minutes):
    if minutes + 5 > 60:
        b = (minutes + 5) % 60
        if hour + 5 >= 24:
            a = (hour + 1) % 24
        else:
            a = hour + 5
    else:
        a = hour
        b = minutes + 5
    schedule.every().day.at("{:02}:{}".format(a,b)).do(second_push_message)
    while True:
        n = schedule.idle_seconds()
        if n is None:
            break
        elif n > 0:
            time.sleep(n)
        schedule.run_pending()