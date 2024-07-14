import json

import aio_pika

from firebase.text import STREAK_1_PUSH_TITLE, STREAK_1_PUSH_BODY

from processors.base import base_process


async def streak_1_process(message: aio_pika.IncomingMessage):
    async with message.process():
        print("Received message from queue:", message.body)
        try:
            data = json.loads(message.body)
            token = data['push_token']
            partner_name = data['partner_name']

            title = STREAK_1_PUSH_TITLE.format(partner_name)
            await base_process(token, title, STREAK_1_PUSH_BODY)
        except Exception as e:
            print(f"Error processing message: {e}")