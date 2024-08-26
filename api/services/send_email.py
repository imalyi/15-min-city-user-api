import requests
from api.config import config


def send_simple_message(*, user_email: str, subject: str, text: str):
    response = requests.post(
        "https://api.eu.mailgun.net/v3/cityinminutes.me/messages",
        auth=("api", config.MAILGUN_API_KEY),
        data={
            "from": "Monika z CityInMinutes.me <mailgun@cityinminutes.me>",
            "to": [user_email],
            "subject": subject,
            "text": text,
        },
    )
