import json

import aio_pika

from firebase.text import (PARTNER_SENT_PIC_BODY, PARTNER_SENT_PIC_TITLE,
                           PARTNER_SENT_PIC_PUSH_NAME, PARTNER_SENT_PIC_LIVE_ACTIVITY_PUSH_NAME,
                           PARTNER_SENT_PIC_LIVE_ACTIVITY_END_PUSH_NAME)

from processors.base import base_process, silent_base_process

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


async def partner_sent_pic_live_activity_process(message: aio_pika.IncomingMessage):
    async with message.process():
        print("Received message from queue:", PARTNER_SENT_PIC_LIVE_ACTIVITY_PUSH_NAME, ' message:', message.body)
        try:
            data = json.loads(message.body)
            token = data['push_token']
            partner_name = data['partner_name']
            apphud_user_id = data.get('apphud_user_id')
            img_url = data['img_url']
            partner_avatar_url = data.get('partner_avatar_url')
            comment = data.get('comment')

            # TODO: refactor this if
            if not comment:
                payload = {
                    'sent_pic': {
                        'img_url': img_url,
                        'partner_avatar_url': partner_avatar_url,
                        'partner_name': partner_name,
                        'action': 'update',
                        'live_activity_type': 'photo'
                    }
                }
            else:
                payload = {
                    'sent_pic': {
                        'img_url': img_url,
                        'partner_avatar_url': partner_avatar_url,
                        'partner_name': partner_name,
                        'comment': comment,
                        'action': 'update',
                        'live_activity_type': 'photo'
                    }
                }

            rabbitmq_client = RabbitMQProducer()

            await silent_base_process(token, payload, PARTNER_SENT_PIC_LIVE_ACTIVITY_PUSH_NAME, rabbitmq_client, apphud_user_id)
        except Exception as e:
            print(f"Error processing message: {e}")


async def partner_sent_pic_live_activity_end_process(message: aio_pika.IncomingMessage):
    async with message.process():
        print("Received message from queue:", PARTNER_SENT_PIC_LIVE_ACTIVITY_END_PUSH_NAME, ' message:', message.body)
        try:
            data = json.loads(message.body)
            token = data['push_token']
            apphud_user_id = data.get('apphud_user_id')

            rabbitmq_client = RabbitMQProducer()

            await silent_base_process(token, {
                'action': 'end',
                'live_activity_type': 'photo'
            }, PARTNER_SENT_PIC_LIVE_ACTIVITY_END_PUSH_NAME, rabbitmq_client, apphud_user_id)
        except Exception as e:
            print(f"Error processing message: {e}")