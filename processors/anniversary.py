import aio_pika

import json

from firebase.text import ANNIVERSARY_PUSH_TITLE, ANNIVERSARY_PUSH_BODY, ANNIVERSARY_PUSH_NAME

from processors.base import base_process


async def anniversary_process(message: aio_pika.IncomingMessage):
    async with message.process():
        print("Received message from queue:", message.body)
        try:
            data = json.loads(message.body)
            token = data['push_token']

            await base_process(token, ANNIVERSARY_PUSH_TITLE, ANNIVERSARY_PUSH_BODY, ANNIVERSARY_PUSH_NAME)
        except Exception as e:
            print(f"Error processing message: {e}")