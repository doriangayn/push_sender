import aio_pika

from processors.base import base_process

from firebase.text import QUESTION_REACTION_PUSH_NAME, QUESTION_REACTION_BODY, QUESTION_REACTION_TITLE

from rabbitmq.rabbitmq import RabbitMQProducer

import json


async def partner_question_reaction_process(message: aio_pika.IncomingMessage):
    async with message.process():
        print("Received message from queue:", QUESTION_REACTION_PUSH_NAME, " messageg", message.body)
        try:
            data = json.loads(message.body)
            token = data['push_token']
            apphud_user_id = data['apphud_user_id']
            partner_name = data["partner_name"]

            rabbitmq_client = RabbitMQProducer()

            title = QUESTION_REACTION_TITLE.format(partner_name)

            await base_process(token, title, QUESTION_REACTION_BODY, QUESTION_REACTION_PUSH_NAME, rabbitmq_client, apphud_user_id)
        except Exception as e:
            print(f"Error processing message: {e}")