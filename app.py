import asyncio

from fastapi import FastAPI

from receiver import ConsumerClient
from services import StatisticServices


class App(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pika_client = ConsumerClient(self.log_incoming_message)

    @classmethod
    async def log_incoming_message(cls, message: dict):
        try:
            print('Incoming message', message)
            await StatisticServices.create_statistic(data=message)
        except Exception as e:
            print(f"Error: {e}")
