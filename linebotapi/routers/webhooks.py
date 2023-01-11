import os
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Header, Request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextMessage, MessageEvent, TextSendMessage, StickerMessage, \
    StickerSendMessage
from pydantic import BaseModel
import uuid

from msg_queues import msgqueues

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

router = APIRouter(
    prefix="/webhooks",
    tags=["chatbot"],
    responses={404: {"description": "Not found"}},
)

class Line(BaseModel):
    destination: str
    events: List[Optional[None]]


@router.post("/line")
async def callback(request: Request, x_line_signature: str = Header(None)):
    body = await request.body()
    try:
        handler.handle(body.decode("utf-8"), x_line_signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="chatbot handle body error.")
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    print("!!!!!!!!!!!!!!!!!!!!!!")
    print(event)
    # bot_mode = msgqueues.bot_mode
    msgqueues.bot_mode = 'linebot'
    lineText = {
        'id': str(uuid.uuid4()),
        'reply_token': event.reply_token,
        'text': event.message.text,
    }
    msgqueues.values.append(lineText)
    print("!!!!!!!!!!!!!!!!!!!!!!")
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=event.message.text+bot_mode)
    # )


# @handler.add(MessageEvent, message=StickerMessage)
# def sticker_text(event):
#     # Judge condition
#     line_bot_api.reply_message(
#         event.reply_token,
#         StickerSendMessage(package_id='6136', sticker_id='10551379')
#     )