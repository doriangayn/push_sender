import aio_pika

import json

from firebase.text import (REACTIVATE_1_PUSH_BODY, REACTIVATE_1_PUSH_TITLE, REACTIVATE_2_PUSH_BODY,
                           REACTIVATE_2_PUSH_TITLE, REACTIVATE_3_PUSH_BODY, REACTIVATE_3_PUSH_TITLE)

from processors.base import base_process


async def reactivation_process(reactivation_title: str, reactivation_body: str, message: aio_pika.IncomingMessage):
    async with message.process():
        print("Received message from queue:", message.body)
        try:
            data = json.loads(message.body)
            token = data['push_token']

            await base_process(token, reactivation_title, reactivation_body)
        except Exception as e:
            print(f"Error processing message: {e}")


async def reactivation_1_process(message: aio_pika.IncomingMessage):
    return await reactivation_process(REACTIVATE_1_PUSH_TITLE, REACTIVATE_1_PUSH_BODY, message)


async def reactivation_2_process(message: aio_pika.IncomingMessage):
    return await reactivation_process(REACTIVATE_2_PUSH_TITLE, REACTIVATE_2_PUSH_BODY, message)


async def reactivation_3_process(message: aio_pika.IncomingMessage):
    return await reactivation_process(REACTIVATE_3_PUSH_TITLE, REACTIVATE_3_PUSH_BODY, message)
