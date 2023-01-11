import uvicorn

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Optional

from msg_queues import msgqueues, MsgItem

from routers import webhooks

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.include_router(webhooks.router)


@app.get("/")
def read_root():
    return {"message": "app bot api"}

@app.post("/values")
async def create_values(item: MsgItem):
    if item.mode.lower() == 'reset':
        msgqueues.bot_mode = ''
        msgqueues.values.clear()
        return {"message": "clear all values"}
    elif item.mode.lower() == msgqueues.bot_mode:
        msgqueues.values.append(item.value)
        return {"message": "value saved in session"}
    else:
        msgqueues.bot_mode = item.mode
        if len(msgqueues.values) > 0:
            msgqueues.values.clear()
        msgqueues.values.append(item.value)
        return {"message": "value saved in new session"}

@app.delete("/value/{id}", status_code=204)
def delete_value(id: str) -> None:
    value_to_remove = find_value(id)

    if value_to_remove is not None:
        msgqueues.values.remove(value_to_remove)

def find_value(id) -> Optional[dict]:
    for value in msgqueues.values:
        if value['id'] == id:
            return value
    return None

@app.get("/values")
async def read_values():
    return {
        "app_name": msgqueues.app_name,
        "bot_mode": msgqueues.bot_mode,
        "values": msgqueues.values,
    }

@app.get("/liff", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)