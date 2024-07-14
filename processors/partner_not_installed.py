import aio_pika

import json

from firebase.text import PARTNER_NOT_INSTALLED_PUSH_TITLE, PARTNER_NOT_INSTALLED_PUSH_BODY

from processors.base import base_process


async def partner_not_installed_process(message: aio_pika.IncomingMessage):
    async with message.process():
        print("Received message from queue:", message.body)
        try:
            data = json.loads(message.body)
            token = data['push_token']

            await base_process(token, PARTNER_NOT_INSTALLED_PUSH_TITLE, PARTNER_NOT_INSTALLED_PUSH_BODY)
        except Exception as e:
            print(f"Error processing message: {e}")