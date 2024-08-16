import json

import aio_pika

from firebase.text import PARTNER_NUDEGED_ABOUT_CHECKUP_TITTLE, PARTNER_NUDEGED_ABOUT_CHECKUP_BODY, PARTNER_NUDGED_PUSH_NAME

from processors.base import base_process

from rabbitmq.rabbitmq import RabbitMQProducer


async def partner_nudged_about_checkup_process(message: aio_pika.IncomingMessage):
    async with message.process():
        print("Received message from queue:", PARTNER_NUDGED_PUSH_NAME, ' message:', message.body)
        try:
            data = json.loads(message.body)
            token = data['push_token']
            partner_name = data['partner_name']
            apphud_user_id = data.get('apphud_user_id')

            rabbitmq_client = RabbitMQProducer()

            title = PARTNER_NUDEGED_ABOUT_CHECKUP_TITTLE.format(partner_name)
            await base_process(token, title, PARTNER_NUDEGED_ABOUT_CHECKUP_BODY, PARTNER_NUDGED_PUSH_NAME, rabbitmq_client, apphud_user_id)
        except Exception as e:
            print(f"Error processing message: {e}")
