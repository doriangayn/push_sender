from firebase.firebase_client import FirebaseClient


async def base_process(token, title, body):
    firebase_client = FirebaseClient()

    await firebase_client.send_push_notification(token, title, body)