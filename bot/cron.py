import schedule
import time
import requests


def job():
    requests.get('https://telegramexpert.ru/api/send/idols/')


# schedule.every(1).minutes.do(job)
schedule.every().hour.do(job)

while True:
    schedule.run_pending()
