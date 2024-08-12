import json

import aio_pika

from firebase.text import PARTNER_INSTALLED_APP_PUSH_TITLE, PARTNER_INSTALLED_APP_PUSH_BODY, PARTNER_INSTALLED_APP_PUSH_NAME

from processors.base import base_process

from rabbitmq.rabbitmq import RabbitMQProducer


async def partner_installed_app_process(message: aio_pika.IncomingMessage):
    async with message.process():
        print("Received message from queue:", PARTNER_INSTALLED_APP_PUSH_NAME, ' message:', message.body)
        try:
            data = json.loads(message.body)
            token = data.get('push_token')

            apphud_user_id = data.get('apphud_user_id')

            rabbitmq_client = RabbitMQProducer()

            await base_process(token, PARTNER_INSTALLED_APP_PUSH_TITLE, PARTNER_INSTALLED_APP_PUSH_BODY, PARTNER_INSTALLED_APP_PUSH_NAME, rabbitmq_client, apphud_user_id)
        except Exception as e:
            print(f"Error processing message: {e}")