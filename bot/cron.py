import schedule
import time
import requests


def job():
    requests.get('http://127.0.0.1:8000/api/send/idols/')


# schedule.every(1).minutes.do(job)
schedule.every().hour.do(job)

while True:
    schedule.run_pending()
