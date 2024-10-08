import aio_pika

import json

from firebase.text import (REACTIVATE_1_PUSH_BODY, REACTIVATE_1_PUSH_TITLE, REACTIVATE_2_PUSH_BODY,
                           REACTIVATE_2_PUSH_TITLE, REACTIVATE_3_PUSH_BODY, REACTIVATE_3_PUSH_TITLE,
                           REACTIVATE_1_PUSH_NAME, REACTIVATE_2_PUSH_NAME, REACTIVATE_3_PUSH_NAME)

from processors.base import base_process
from rabbitmq.rabbitmq import RabbitMQProducer


async def reactivation_process(reactivation_title: str, reactivation_body: str, message: aio_pika.IncomingMessage, push_name: str, rabbitmq_client):
    async with message.process():
        print("Received message from queue:", push_name, " message:", message.body)
        try:
            data = json.loads(message.body)
            token = data['push_token']
            apphud_user_id = data.get('apphud_user_id')

            await base_process(token, reactivation_title, reactivation_body, push_name, rabbitmq_client, apphud_user_id)
        except Exception as e:
            print(f"Error processing message: {e}")


async def reactivation_1_process(message: aio_pika.IncomingMessage):
    rabbitmq_client = RabbitMQProducer()
    return await reactivation_process(REACTIVATE_1_PUSH_TITLE, REACTIVATE_1_PUSH_BODY, message, REACTIVATE_1_PUSH_NAME, rabbitmq_client)


async def reactivation_2_process(message: aio_pika.IncomingMessage):
    rabbitmq_client = RabbitMQProducer()

    return await reactivation_process(REACTIVATE_2_PUSH_TITLE, REACTIVATE_2_PUSH_BODY, message, REACTIVATE_2_PUSH_NAME, rabbitmq_client)


async def reactivation_3_process(message: aio_pika.IncomingMessage):
    rabbitmq_client = RabbitMQProducer()

    return await reactivation_process(REACTIVATE_3_PUSH_TITLE, REACTIVATE_3_PUSH_BODY, message, REACTIVATE_3_PUSH_NAME, rabbitmq_client)
