import aio_pika

import json

from firebase.text import PARTNER_NOT_INSTALLED_PUSH_TITLE, PARTNER_NOT_INSTALLED_PUSH_BODY, PARTNER_NOT_INSTALLED_PUSH_NAME

from processors.base import base_process

from rabbitmq.rabbitmq import RabbitMQProducer


async def partner_not_installed_process(message: aio_pika.IncomingMessage):
    async with message.process():
        print("Received message from queue:", PARTNER_NOT_INSTALLED_PUSH_NAME, " messageg", message.body)
        try:
            data = json.loads(message.body)
            token = data['push_token']
            apphud_user_id = data['apphud_user_id']

            rabbitmq_client = RabbitMQProducer()

            await base_process(token, PARTNER_NOT_INSTALLED_PUSH_TITLE, PARTNER_NOT_INSTALLED_PUSH_BODY, PARTNER_NOT_INSTALLED_PUSH_NAME, rabbitmq_client, apphud_user_id)
        except Exception as e:
            print(f"Error processing message: {e}")