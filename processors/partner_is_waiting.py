import json

import aio_pika

from firebase.text import PARTNER_IS_WAITING_PUSH_TITLE, PARTNER_IS_WAITING_PUSH_BODY, PARTNER_IS_WAITING_PUSH_NAME

from processors.base import base_process

from rabbitmq.rabbitmq import RabbitMQProducer


async def partner_is_waiting_process(message: aio_pika.IncomingMessage):
    async with message.process():
        print("Received message from queue:", PARTNER_IS_WAITING_PUSH_NAME, ' message:', message.body)
        try:
            data = json.loads(message.body)

            token = data['push_token']
            partner_name = data['partner_name']
            apphud_user_id = data.get('apphud_user_id')
            question_id = str(data.get('question_id', None))

            rabbitmq_client = RabbitMQProducer()

            custom_data = {"question_id": question_id}

            title = PARTNER_IS_WAITING_PUSH_TITLE.format(partner_name)
            await base_process(token, title, PARTNER_IS_WAITING_PUSH_BODY, PARTNER_IS_WAITING_PUSH_NAME, rabbitmq_client, apphud_user_id, custom_data)
        except Exception as e:
            print(f"Error processing message: {e}")
