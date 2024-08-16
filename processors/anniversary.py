import aio_pika

import json

from firebase.text import ANNIVERSARY_PUSH_TITLE, ANNIVERSARY_PUSH_BODY, ANNIVERSARY_PUSH_NAME

from processors.base import base_process

from rabbitmq.rabbitmq import RabbitMQProducer


async def anniversary_process(message: aio_pika.IncomingMessage, rabbitmq_client):
    async with message.process():
        print("Received message from queue:", ANNIVERSARY_PUSH_NAME, ' message', message.body)
        try:
            data = json.loads(message.body)
            token = data['push_token']
            apphud_user_id = data.get('apphud_user_id')

            rabbitmq_client = RabbitMQProducer()

            await base_process(token, ANNIVERSARY_PUSH_TITLE, ANNIVERSARY_PUSH_BODY, ANNIVERSARY_PUSH_NAME, rabbitmq_client, apphud_user_id)
        except Exception as e:
            print(f"Error processing message: {e}")