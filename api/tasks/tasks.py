from api.tasks.celery import celery
from api.addresses.router import get_address_by_id


@celery.task
def generate_report(address: str):
    print(address)
