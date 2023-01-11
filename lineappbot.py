from asyncio import gather, sleep
import time
import httpx
import json
from linebot import LineBotApi
from lineappbothandler import appbot_handler
from linebot.models import TextSendMessage

class LineAppBot(object):
    def __init__(self, api_root, line_channel_access_token):
        """__init__ method.
        """
        self._api_root = api_root
        self._line_channel_access_token = line_channel_access_token

        self._line_bot_api = LineBotApi(line_channel_access_token)

    async def async_request(self, method, url, headers={}, payload={}):
        method = method.lower()
        async with httpx.AsyncClient() as client:
            if method == 'get':
                # print(url)
                resp = await client.get(url, headers=headers)
                # print(resp)
                result = resp.json()
            elif method == 'post':
                resp = await client.post(url, headers=headers, data=payload)
                result = resp.json()
            elif method == 'delete':
                resp = await client.delete(url, headers=headers)
                # print(resp)
                result = None
            else:
                result = None
            return result

    async def get_values(self):
        url = self._api_root + '/values'

        return await self.async_request('GET', url)

    async def clear_values(self):
        url = self._api_root + '/values'
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {
            "mode": "reset",
            "value": {}
        }

        return await self.async_request('POST', url, headers=headers, payload=json.dumps(data))

    async def delete_value(self, id):
        url = self._api_root + '/value/' + id

        return await self.async_request('DELETE', url)

    async def reply_bot(self, item):
        print(item)
        await appbot_handler.handle(item)
        resp = await self.delete_value(item['id'])

    async def poll(self, time_wait):
        try:
            print('reset', await self.clear_values())

            start_poll = time.time()
            next_poll = start_poll - (start_poll % time_wait) # ตั้งรอบเวลา
            while True:
                seconds = time.time()
                if seconds >= next_poll: # ครบรอบ
                    values = await self.get_values()
                    t2=time.time()-seconds
                    # print(f'\r{t2:0.2f} secs {values}', end='')
                    # print(f'{t2:0.2f} secs {values}')
                    # loops = [self.reply_bot(item) for item in values['values']]
                    # await gather(*loops)
                    for item in values['values']:
                        await self.reply_bot(item)
                    next_poll += time_wait # กำหนดรอบเวลาถัดไป
                await sleep(1)
        except KeyboardInterrupt:
            pass

        except Exception as ex:
            print(type(ex).__name__, str(ex))

    def reply_message(self, reply_token, reply_message):
        self._line_bot_api.reply_message(
            reply_token,
            TextSendMessage(text=reply_message)
        )