import os
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=14)
def keep_alive():
    try:
        app_url = f"https://{os.getenv('HEROKU_APP_NAME')}.herokuapp.com/"
        response = requests.get(app_url)
        print(f"Keep-alive ping sent, status: {response.status_code}")
    except Exception as e:
        print(f"Keep-alive failed: {e}")

if __name__ == '__main__':
    sched.start()
