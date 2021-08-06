import requests
import time
from aiogram import Bot, Dispatcher, types
import aiogram.utils.markdown as fmt


def send_message():
    method = "sendMessage"
    token = "1921418522:AAGhuuELsBbOeby0OcjyjlGO5lqAbypl30c"
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"chat_id": 866200119,
            "text": f"hello {fmt.hide_link('https://get.wallhere.com/photo/2560x1600-px-ancient-architecture-castle-field-forest-Germany-hill-Hohenzollern-landscape-nature-sky-tower-trees-x-px-661906.jpg')}", "parse_mode": types.ParseMode.HTML}
    for i in range(0, 10):
        time.sleep(3)
        requests.post(url, data=data)


send_message()
