import json

import aio_pika

from firebase.text import PARTNER_INSTALLED_APP_PUSH_TITLE, PARTNER_INSTALLED_APP_PUSH_BODY

from processors.base import base_process


async def partner_installed_app_process(message: aio_pika.IncomingMessage):
    async with message.process():
        print("Received message from queue:", message.body)
        try:
            data = json.loads(message.body)
            token = data['push_token']
            partner_name = data['partner_name']

            title = PARTNER_INSTALLED_APP_PUSH_TITLE.format(partner_name)
            await base_process(token, title, PARTNER_INSTALLED_APP_PUSH_BODY)
        except Exception as e:
            print(f"Error processing message: {e}")