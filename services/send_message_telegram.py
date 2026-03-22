import requests
import logging
import os
from models.alerta import Alerta
from services.message_constructor import message_constructor

token = os.environ.get("TELEGRAM_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")


def send_message(novo_erro: Alerta) -> str:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
    "chat_id": chat_id,
    "text": message_constructor(novo_erro),
    "parse_mode": "HTML"
    }

    r = requests.post(url, json=payload)
    logging.info(r.status_code)
    logging.info(r.text)

    return "Mensagem enviada ao plantonista com sucesso"

