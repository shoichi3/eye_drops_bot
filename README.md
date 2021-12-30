# 目薬通知bot
目薬通知botは特定の時間に通知を送るためのbotです．機能としてはpush通知の他にメッセージのやり取りも行うことができます．なお，特定の時間に通知を送るためGithub actionsを用いています．

# なぜ作成したのか
母がドライアイで毎日定期的に目薬を指す必要があるが，よく「忘れてた」と言っていました．そこで，特定の時間に母に通知を送ることができればこの問題を解決することができるのではないかと考え，この通知botを作成しました．

# 使用技術
### バックエンド
Python 3.9.1
Django 3.2.7
### API
LINE Messaging API
### 本番環境
Heroku

# インフラ構成図
<img width="719" alt="スクリーンショット 2021-09-20 16 14 17" src="https://user-images.githubusercontent.com/69130053/133967629-63a28103-6ae2-41bf-9202-a2cd808cb305.png">
