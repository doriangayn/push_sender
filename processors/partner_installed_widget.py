import json

import aio_pika

from firebase.text import PARTNER_INSTALLED_WIDGET_TITLE, PARTNER_INSTALLED_WIDGET_BODY, PARTNER_INSTALLED_WIDGET_PUSH_NAME

from processors.base import base_process

from rabbitmq.rabbitmq import RabbitMQProducer


async def partner_installed_widget_process(message: aio_pika.IncomingMessage):
    async with message.process():
        print("Received message from queue:", PARTNER_INSTALLED_WIDGET_PUSH_NAME, ' message:', message.body)
        try:
            data = json.loads(message.body)
            token = data['push_token']
            partner_name = data['partner_name']

            apphud_user_id = data.get('apphud_user_id')

            title = PARTNER_INSTALLED_WIDGET_TITLE.format(partner_name)
            body = PARTNER_INSTALLED_WIDGET_BODY.format(partner_name)


            rabbitmq_client = RabbitMQProducer()

            await base_process(token, title, body, PARTNER_INSTALLED_WIDGET_PUSH_NAME, rabbitmq_client, apphud_user_id)
        except Exception as e:
            print(f"Error processing message: {e}")