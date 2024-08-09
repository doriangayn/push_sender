import aio_pika

import json

from firebase.text import LOST_ONBO_PUSH_TITLE, LOST_ONBO_PUSH_BODY, LOST_ONBO_PUSH_NAME

from processors.base import base_process

from rabbitmq.rabbitmq import RabbitMQProducer


async def lost_onbo_process(message: aio_pika.IncomingMessage):
    async with message.process():
        print("Received message from queue:", LOST_ONBO_PUSH_NAME, ' message:', message.body)
        try:
            data = json.loads(message.body)
            token = data['push_token']
            apphud_user_id = data.get('apphud_user_id')

            rabbitmq_client = RabbitMQProducer()

            await base_process(token, LOST_ONBO_PUSH_TITLE, LOST_ONBO_PUSH_BODY, LOST_ONBO_PUSH_NAME, rabbitmq_client, apphud_user_id)
        except Exception as e:
            print(f"Error processing message: {e}")