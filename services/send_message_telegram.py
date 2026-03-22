import requests
import logging
import os

token = os.environ.get("TELEGRAM_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")


def send_message(mensagem: str) -> int:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
    "chat_id": chat_id,
    "text": mensagem
    }

    r = requests.post(url, json=payload)
    logging.info(r.status_code)
    logging.info(r.text)

    return r.status_code

