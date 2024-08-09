import asyncio
import aio_pika

from rabbitmq.constants import ANALYTICS_SEND_PUSH_SEND_QUEUE_NAME


class RabbitMQConsumer:
    def __init__(self, rabbitmq_url, queue_callbacks):
        self.queue_callbacks = queue_callbacks
        self.connection = None
        self.channels = []
        self.queues = []
        self.rabbitmq_url = rabbitmq_url

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.rabbitmq_url, ssl=False, ssl_options={})
        for queue_name in self.queue_callbacks.keys():
            channel = await self.connection.channel()
            queue = await channel.declare_queue(queue_name, durable=True)
            self.channels.append(channel)
            self.queues.append(queue)

    async def consume(self):
        for queue, callback in zip(self.queues, self.queue_callbacks.values()):
            await queue.consume(callback)
        print('Waiting for messages')
        try:
            await asyncio.Future()  # Run forever
        finally:
            await self.connection.close()


class RabbitMQProducer:
    _instance = None

    def __new__(cls, rabbitmq_url=None):
        if cls._instance is None:
            if rabbitmq_url is None:
                raise ValueError("First initialization requires a rabbitmq_url.")
            cls._instance = super(RabbitMQProducer, cls).__new__(cls)
            cls._instance.rabbitmq_url = rabbitmq_url
            cls._instance.connection = None
            cls._instance.channel = None
        return cls._instance

    async def connect(self):
        if not self.connection:
            self.connection = await aio_pika.connect_robust(self.rabbitmq_url)
            self.channel = await self.connection.channel()

    async def _send_message(self, queue_name, message):
        print('send message to rabbitmq queue_name:', queue_name)
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=message.encode()),
            routing_key=queue_name
        )

    async def send_analytics_push_send(self, message):
        await self._send_message(ANALYTICS_SEND_PUSH_SEND_QUEUE_NAME, message)

    async def close(self):
        if self.connection:
            await self.connection.close()
            self.connection = None
            self.channel = None

