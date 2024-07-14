import asyncio
import aio_pika


class RabbitMQConsumer:
    def __init__(self, rabbitmq_url, queue_callbacks):
        self.queue_callbacks = queue_callbacks
        self.connection = None
        self.channels = []
        self.queues = []
        self.rabbitmq_url = rabbitmq_url

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.rabbitmq_url)
        for queue_name in self.queue_callbacks.keys():
            channel = await self.connection.channel()
            queue = await channel.declare_queue(queue_name, durable=True)
            self.channels.append(channel)
            self.queues.append(queue)

    async def consume(self):
        for queue, callback in zip(self.queues, self.queue_callbacks.values()):
            await queue.consume(callback, no_ack=True)
        print('Waiting for messages. To exit press CTRL+C')
        try:
            await asyncio.Future()  # Run forever
        finally:
            await self.connection.close()