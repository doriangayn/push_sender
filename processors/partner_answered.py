import json

import aio_pika

from firebase.text import PARTNER_ANSWERED_PUSH_TITLE, PARTNER_ANSWERED_PUSH_BODY, PARTNER_ANSWERED_PUSH_NAME

from processors.base import base_process


async def partner_answered_process(message: aio_pika.IncomingMessage):
    async with message.process():
        print("Received message from queue:", message.body)
        try:
            data = json.loads(message.body)
            token = data['push_token']
            partner_name = data['partner_name']

            title = PARTNER_ANSWERED_PUSH_TITLE.format(partner_name)
            await base_process(token, title, PARTNER_ANSWERED_PUSH_BODY, PARTNER_ANSWERED_PUSH_NAME)
        except Exception as e:
            print(f"Error processing message: {e}")