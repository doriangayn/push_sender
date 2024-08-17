import json

import aio_pika

from firebase.text import BOTH_PARTNERS_COMPLETED_CHECKUP_PUSH_NAME, BOTH_PARTNERS_COMPLETED_CHECKUP_TITLE, BOTH_PARTNERS_COMPLETED_CHECKUP_BOOY

from processors.base import base_process

from rabbitmq.rabbitmq import RabbitMQProducer


async def both_partners_completed_checkup(message: aio_pika.IncomingMessage):
    async with message.process():
        print("Received message from queue:", BOTH_PARTNERS_COMPLETED_CHECKUP_PUSH_NAME, ' message:', message.body)
        try:
            data = json.loads(message.body)
            token = data['push_token']
            partner_name = data['partner_name']
            apphud_user_id = data.get('apphud_user_id')

            title = BOTH_PARTNERS_COMPLETED_CHECKUP_TITLE.format(partner_name)
            rabbitmq_client = RabbitMQProducer()
            await base_process(token, title, BOTH_PARTNERS_COMPLETED_CHECKUP_BOOY, BOTH_PARTNERS_COMPLETED_CHECKUP_PUSH_NAME, rabbitmq_client, apphud_user_id)
        except Exception as e:
            print(f"Error processing message: {e}")