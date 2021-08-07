import schedule
import time
import requests


def job():
    requests.get('http://server:8000/api/send/idols/')


# schedule.every(1).minutes.do(job)
schedule.every().hour.do(job)

while True:
    schedule.run_pending()
