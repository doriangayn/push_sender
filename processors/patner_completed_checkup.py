import json

import aio_pika

from firebase.text import PARNTER_COMPLETED_CHECKUP_BODY, PARTNER_COMPLETED_CHECKUP_TITLE, PARTNER_COMPELTED_CHECKUP_PUSH_NAME

from processors.base import base_process

from rabbitmq.rabbitmq import RabbitMQProducer


async def partner_completed_checkup(message: aio_pika.IncomingMessage):
    async with message.process():
        print("Received message from queue:", PARTNER_COMPELTED_CHECKUP_PUSH_NAME, ' message:', message.body)
        try:
            data = json.loads(message.body)
            token = data['push_token']
            partner_name = data['partner_name']
            apphud_user_id = data.get('apphud_user_id')

            title = PARTNER_COMPLETED_CHECKUP_TITLE.format(partner_name)
            rabbitmq_client = RabbitMQProducer()
            await base_process(token, title, PARNTER_COMPLETED_CHECKUP_BODY, PARTNER_COMPELTED_CHECKUP_PUSH_NAME, rabbitmq_client, apphud_user_id)
        except Exception as e:
            print(f"Error processing message: {e}")