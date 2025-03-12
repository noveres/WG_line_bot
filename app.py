from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    ButtonsTemplate,
    PostbackAction,
    TemplateMessage,
    MulticastRequest,
    StickerMessage,  
    ImageMessage,     
    VideoMessage,     
    AudioMessage,     
    LocationMessage,  
    Emoji,
    FlexMessage,  
    TemplateMessage,
    ConfirmTemplate,
    ButtonsTemplate,
    CarouselTemplate,
    CarouselColumn,
    ImageCarouselTemplate,
    ImageCarouselColumn,        

  
  
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    FollowEvent,
    PostbackEvent,
    )
from datetime import datetime

app = Flask(__name__)

configuration = Configuration(access_token='87c0KHHgqJone/4LjtdRsg64+cbgjwCXTdKwvpzDMD2+OttIrhylZbO/n/fegjdA23Idmnw3qmQPjeLtQqyENLDPCtfJil1Z33XA/W1eUi1FZBfPfGy/nLBUFM3tg1sG3YPybhuHI53h0CLtjnOyIgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('21ea6980ef605cc17da34964e6f5366e')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# # 加入好友事件
@handler.add(FollowEvent)
def handle_follow(event):
    print(f"Got follow event: {event}")
    # do something


# 訊息事件
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        user_text = event.message.text  # 抓取使用者輸入的文字
        
        if user_text == '測試用':
            buttons_template = ButtonsTemplate(
                title='超可愛的吉哇哇',
                text='(๑•̀ㅂ•́)و✧',
                actions=[
                    PostbackAction(label='輕輕按下去', text='被咬了', data='postback'),
                ])
            template_message = TemplateMessage(
                alt_text='Postback Sample',
                template=buttons_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[template_message]
                )
            )
        elif user_text == '(被咬了)':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text='吉度憤怒')]
                )
            )
            
        elif user_text == '按鈕':
            confirm_template = ConfirmTemplate(
                title='超可愛的吉哇哇',
                text='你確定要按下按鈕嗎？',
                actions=[
                    PostbackAction(label='是', text='是', data='postback'),
                    PostbackAction(label='否', text='否', data='postback')

                ]

            )
            template_message = TemplateMessage(
                alt_text='Confirm alt text',
                template=confirm_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[template_message]
                )
            )


        elif user_text == '文字':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="這是文字訊息")]
                )
            )

        elif user_text == '表情符號':
            emojis = [
                Emoji(index=0, product_id="5ac1bfd5040ab15980c9b435", emoji_id="001"),
                Emoji(index=12, product_id="5ac1bfd5040ab15980c9b435", emoji_id="002")
            ]
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text='$ LINE 表情符號 $', emojis=emojis)]
                )
            )

        elif user_text == '貼圖':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[StickerMessage(package_id="446", sticker_id="1988")]
                )
            )

        elif user_text == '圖片':
            url = request.url_root + 'static/Logo.jpg'
            url = url.replace("http", "https")
            app.logger.info("url=" + url)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        ImageMessage(original_content_url=url, preview_image_url=url)
                    ]
                )
            )

        elif user_text == '影片':
            url = request.url_root + 'static/video.mp4'
            url = url.replace("http", "https")
            app.logger.info("url=" + url)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        VideoMessage(original_content_url=url, preview_image_url=url)
                    ]
                )
            )

        elif user_text == '音訊':
            url = request.url_root + 'static/music.mp3'
            url = url.replace("http", "https")
            app.logger.info("url=" + url)
            duration = 60000  # in milliseconds
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        AudioMessage(original_content_url=url, duration=duration)
                    ]
                )
            )

        elif user_text == '位置':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        LocationMessage(title='Location', address="Taipei", latitude=25.0475, longitude=121.5173)
                    ]
                )
            )
   
        else:
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=user_text)]
                )
            )




@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'postback':
        print('Postback event is triggered')

if __name__ == "__main__":
    app.run()

    # 來源 https://pypi.org/project/line-bot-sdk/
