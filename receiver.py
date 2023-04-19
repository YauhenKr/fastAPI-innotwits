import json
import pika

from aio_pika import connect_robust


class ConsumerClient:
    PARAMETERS = pika.URLParameters('amqp://admin:admin@rabbit:5672')

    def __init__(self, process_callable):
        self.queue_name = 'hello'
        self.connection = pika.BlockingConnection(self.PARAMETERS)
        self.channel = self.connection.channel()
        self.queue = self.channel.queue_declare(self.queue_name)
        self.callback_queue = self.queue.method.queue
        self.process_callable = process_callable
        print('Pika connection initialized')

    async def consume(self, loop):
        connection = await connect_robust(
            'amqp://admin:admin@rabbit:5672',
            loop=loop
        )
        channel = await connection.channel()
        queue = await channel.declare_queue('hello')
        await queue.consume(self.process_incoming_message, no_ack=False)
        print('Established pika async listener')
        return connection

    async def process_incoming_message(self, message):
        await message.ack()
        body = message.body
        if body:
            await self.process_callable(json.loads(body))
