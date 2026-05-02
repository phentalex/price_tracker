import httpx
from django.conf import settings


def send_tg_alert(chat_id, text):
    url = f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage'
    resp = httpx.post(url, json={'chat_id': chat_id, 'text': text})
    if not resp.is_success:
        print(f'[TG ERROR] {resp.status_code}: {resp.text}', flush=True)