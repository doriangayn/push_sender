import json

import aio_pika

from firebase.text import (
    SENT_LIVE_ACTIVITY_UPDATE_PUSH_NAME
)

from processors.base import base_process, silent_base_process

from rabbitmq.rabbitmq import RabbitMQProducer


async def update_live_activity_process(message: aio_pika.IncomingMessage):
    async with message.process():
        print("Received message from queue:", SENT_LIVE_ACTIVITY_UPDATE_PUSH_NAME, ' message:', message.body)
        try:
            data = json.loads(message.body)
            token = data['push_token']
            apphud_user_id = data.get('apphud_user_id')

            payload = remove_none_values(data.copy())

            rabbitmq_client = RabbitMQProducer()

            await silent_base_process(token, payload, SENT_LIVE_ACTIVITY_UPDATE_PUSH_NAME, rabbitmq_client,
                                      apphud_user_id)
        except Exception as e:
            print(f"Error processing message: {e}")



# TODO: we need this???
# async def end_live_activity_process(message: aio_pika.IncomingMessage):
#     async with message.process():
#         print("Received message from queue:", PARTNER_SENT_PIC_LIVE_ACTIVITY_END_PUSH_NAME, ' message:', message.body)
#         try:
#             data = json.loads(message.body)
#             token = data['push_token']
#             apphud_user_id = data.get('apphud_user_id')
#
#             rabbitmq_client = RabbitMQProducer()
#
#             await silent_base_process(token, {
#                 'action': 'end',
#                 'live_activity_type': 'photo'
#             }, PARTNER_SENT_PIC_LIVE_ACTIVITY_END_PUSH_NAME, rabbitmq_client, apphud_user_id)
#         except Exception as e:
#             print(f"Error processing message: {e}")
def remove_none_values(d: dict) -> dict:
    """Удаляет ключи с None значениями из словаря"""
    return {k: v for k, v in d.items() if v is not None}
