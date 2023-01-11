# emabot_v2

## linebotapi

ใช้เป็นตัวกลางเชื่อต่อระหว่าง line app กับ bot app

    concept:

        line app <=======> linebotapi <=======> bot app
                  webhook              fastapi

api free host แนะนำให้ใช้ https://www.deta.sh/ ให้ทำการสมัครสมาชิกเพื่อใช้งาน

## setup
1. ติดตั้ง linebotapi ที่ https://www.deta.sh/ (https://fastapi.tiangolo.com/deployment/deta/)
    * Install the CLI
    * Login with the CLI
    * Deploy with Deta -> จะได้รับ url เป็นรูปแบบ https://<code\>.deta.dev
    * Rename sample.env to .env and set value LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET and run command

        deta update -e .env

    * Test API
2. สร้าง line bot แบบ Messageing API
3. กำหนด webhook url เป็น url https://<code\>.deta.dev/webhooks/line ที่ได้รับจาก https://www.deta.sh/
4. สร้าง bot app ตามตัวอย่าง sample_bot.py