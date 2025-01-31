# app/tasks.py
from celery import Celery
from database import add_to_db
from models import AccessLog
import os

REDIS_URL = os.environ.get('REDIS_URL','redis://localhost:6379/0')

# Setup Celery
celery = Celery(__name__, broker=REDIS_URL, backend=REDIS_URL)

# Task to log access
@celery.task
def save_access_log_task(log_text):
    try:
        log = AccessLog(text=log_text)
        add_to_db(log)
        print('successfully logged rn')
    except:
        print('Could not log')
