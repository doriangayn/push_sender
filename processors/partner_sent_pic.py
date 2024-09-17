import json

import aio_pika

from firebase.text import PARTNER_SENT_PIC_BODY, PARTNER_SENT_PIC_TITLE, PARTNER_SENT_PIC_PUSH_NAME

from processors.base import base_process

from rabbitmq.rabbitmq import RabbitMQProducer


async def partner_sent_pic_process(message: aio_pika.IncomingMessage):
    async with message.process():
        print("Received message from queue:", PARTNER_SENT_PIC_PUSH_NAME, ' message:', message.body)
        try:
            data = json.loads(message.body)
            token = data['push_token']
            partner_name = data['partner_name']
            apphud_user_id = data.get('apphud_user_id')

            title = PARTNER_SENT_PIC_TITLE.format(partner_name)

            rabbitmq_client = RabbitMQProducer()

            await base_process(token, title, PARTNER_SENT_PIC_BODY, PARTNER_SENT_PIC_PUSH_NAME, rabbitmq_client, apphud_user_id)
        except Exception as e:
            print(f"Error processing message: {e}")