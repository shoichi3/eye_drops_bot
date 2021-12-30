from linebot.models import TemplateSendMessage,ConfirmTemplate,MessageAction

def push_message(number, action1, action2):
  message = TemplateSendMessage(
                                alt_text='目薬の時間です',
                                template=ConfirmTemplate(
                                    text=('{}つ目の目薬を打ちましたか？').format(number),
                                    actions=[
                                        MessageAction(
                                            label=('{}').format(action1),
                                            text=('{}').format(action1)
                                        ),
                                        MessageAction(
                                            label=('{}').format(action2),
                                            text=('{}').format(action2)
                                        )
                                    ]
                                )
                            )
  return message