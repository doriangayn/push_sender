import json

from firebase.firebase_client import FirebaseClient


async def base_process(token, title, body, push_name, rabbitmq_client, apphud_user_id, custom_data):
    if token is None:
        return

    firebase_client = FirebaseClient()

    await firebase_client.send_push_notification(token, title, body, push_name, custom_data)

    analytics_message = json.dumps({
        'push_name': push_name,
        'push_title': title,
        'push_subtitle': body,
        'apphud_user_id': apphud_user_id
    })

    await rabbitmq_client.connect()
    await rabbitmq_client.send_analytics_push_send(analytics_message)


async def silent_base_process(token, payload, push_name, rabbitmq_client, apphud_user_id):
    if token is None:
        return

    payload['push_name'] = push_name

    firebase_client = FirebaseClient()

    await firebase_client.send_silent_push_notification(token, payload)

    analytics_message = json.dumps({
        'push_name': push_name,
        'apphud_user_id': apphud_user_id
    })

    await rabbitmq_client.connect()
    await rabbitmq_client.send_analytics_push_send(analytics_message)

