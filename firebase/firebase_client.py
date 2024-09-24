import os

import firebase_admin
from firebase_admin import credentials, messaging
import asyncio


class FirebaseClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cred = credentials.Certificate(os.getenv("FIREBASE_SECRETS_JSON_PATH"))
            cls._instance.app = firebase_admin.initialize_app(cred)
        return cls._instance

    async def send_push_notification(self, token, title, body, push_name):
        custom_data = {'push_name': push_name}
        message = messaging.Message(
            data=custom_data,
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
            apns=messaging.APNSConfig(payload=messaging.APNSPayload(
                aps=messaging.Aps(content_available=True, custom_data={'data': custom_data}))))

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, messaging.send, message)
        print('Successfully sent message:', response)

    async def send_silent_push_notification(self, token, payload):
        custom_data = payload
        message = messaging.Message(
            data=custom_data,
            token=token,
            apns=messaging.APNSConfig(
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(content_available=True)  # Устанавливаем флаг сайлент-пуша
                ),
                headers={
                    'apns-priority': '10',  # Высокий приоритет доставки для iOS
                }
            ),
            # TODO: мб понадобится
            # android=messaging.AndroidConfig(
            #     priority="high",  # Для Android нужно указать высокий приоритет
            #     data=custom_data  # Передаем данные в Android
            # )
        )

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, messaging.send, message)
        print('Successfully sent silent push:', response)

    async def send_multicast_push_notification(self, tokens, title, body):
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            tokens=tokens,
        )

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, messaging.send_multicast, message)
        print('Successfully sent message:', response.success_count, 'messages were sent successfully')
