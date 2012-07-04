from celery.task import task
from main.utils import process_data_queue


@task()
def process_dqueue():
    process_data_queue()