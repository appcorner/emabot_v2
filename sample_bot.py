from asyncio import get_event_loop, sleep
from lineappbot import LineAppBot
from lineappbothandler import appbot_handler

API_ROOT = 'https://<code>.deta.dev'
LINE_CHANNEL_ACCESS_TOKEN = '<line_channel_access_token>'

appbot = LineAppBot(API_ROOT, LINE_CHANNEL_ACCESS_TOKEN)

async def main():
    
    while True:

        print('bot running...')

        # implement your program

        await sleep(60)

#---------------------
# bot command handler
#---------------------

@appbot_handler.add(commands=['command_error'])
def command_error(item):
    appbot.reply_message(
        item['reply_token'],
        'กรุณาตรวจสอบคำสั่งของท่านอีกครั้ง'
    )

@appbot_handler.add(commands=['show_balance','แสดงบัญชี'])
def show_balance(item):
    appbot.reply_message(
        item['reply_token'],
        'ผลประกอบการของท่าน...'
    )

@appbot_handler.add(commands='show_setting')
def show_setting(item):
    appbot.reply_message(
        item['reply_token'],
        'setting ของท่าน...'
    )

if __name__ == "__main__":
    try:
        loop = get_event_loop()
        loop.create_task(appbot.poll(5))
        loop.run_until_complete(main()) 
    
    except KeyboardInterrupt:
        print('bye')

    except Exception as ex:
        print(type(ex).__name__, str(ex))

    finally:
        print('end')