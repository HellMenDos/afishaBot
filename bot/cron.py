import schedule
import time
import requests


def job():
    requests.get('http://admin:8000/api/send/idols/')


schedule.every().hour.do(job)

while True:
    schedule.run_pending()
