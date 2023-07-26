import os
import time
from celery import Celery, shared_task

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
app = Celery('myapp', broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')


@celery.task(name='tasks.add')
def add(x: int, y: int) -> int:
    time.sleep(5)
    return x + y


@app.task
def my_flask_task(param1, param2):
    time.sleep(5)
    return param1 + param2



@app.task(queue='ml_queue')
@shared_task
def run_ml_task(data):
    result = "ML Task Result: " + data
    print(result)
    return result

