import requests
import time
from aiogram import Bot, Dispatcher, types
import aiogram.utils.markdown as fmt


def send_message():
    method = "sendMessage"
    token = "1921418522:AAGhuuELsBbOeby0OcjyjlGO5lqAbypl30c"
    url = f"https://api.telegram.org/bot{token}/sendlocation?chat_id=866200119&latitude=51.6680&longitude=32.6546"
    requests.post(url)


send_message()
