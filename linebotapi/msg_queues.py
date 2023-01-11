from pydantic import BaseModel

class MsgQueues(BaseModel):
    app_name: str = "APP Bot API"
    bot_mode: str = ""
    values: list[dict] = []

class MsgItem(BaseModel):
    mode: str
    value: dict

msgqueues = MsgQueues()