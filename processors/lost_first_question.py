import aio_pika

import json

from firebase.text import LOST_FIRST_QUESTION_PUSH_TITLE, LOST_FIRST_QUESTION_PUSH_BODY

from processors.base import base_process


async def lost_first_question_process(message: aio_pika.IncomingMessage):
    async with message.process():
        print("Received message from queue:", message.body)
        try:
            data = json.loads(message.body)
            token = data['push_token']

            await base_process(token, LOST_FIRST_QUESTION_PUSH_TITLE, LOST_FIRST_QUESTION_PUSH_BODY)
        except Exception as e:
            print(f"Error processing message: {e}")