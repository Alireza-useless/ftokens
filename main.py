from json import loads, dumps
from time import sleep
from websocket import WebSocket
from concurrent.futures import ThreadPoolExecutor

# مشخصات گیلد و چنل ثابت
guild_id = "1182277701877366834"  # گیلد
chid = "1182279162241749042"  # چنل

# خواندن توکن‌ها از فایل
tokenlist = open("tokens.txt").read().splitlines()
executor = ThreadPoolExecutor(max_workers=10)  # تعداد کارگرها را کمتر کنید


def run(token):
    try:
        # اتصال به WebSocket
        ws = WebSocket()
        ws.connect("wss://gateway.discord.gg/?v=8&encoding=json")
        hello = loads(ws.recv())
        heartbeat_interval = hello['d']['heartbeat_interval']

        # ارسال پیام‌های اولیه برای اتصال به سرور
        ws.send(
            dumps({
                "op": 2,
                "d": {
                    "token": token,
                    "properties": {
                        "$os": "windows",
                        "$browser": "Discord",
                        "$device": "desktop"
                    }
                }
            }))
        ws.send(
            dumps({
                "op": 4,
                "d": {
                    "guild_id": guild_id,
                    "channel_id": chid
                }
            }))  # فقط اتصال به چنل و گیلد

        while True:
            sleep(heartbeat_interval / 1000)
            try:
                ws.send(dumps({"op": 1, "d": None}))  # ارسال ضربان قلب
            except Exception:
                break  # در صورت بروز خطا، اتصال قطع می‌شود و باید دوباره وصل شود
    except Exception as e:
        print(f"Error: {e}")


# اجرا برای تمامی توکن‌ها از فایل tokens.txt
i = 0
for token in tokenlist:
    executor.submit(run, token)
    i += 1
    print(f"connected ws: {i}")
