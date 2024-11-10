import asyncio
import json

import structlog


class PlainTerminal:
    def __init__(self, input_client):
        self.logger = structlog.get_logger().bind()
        input_client.listeners.append(self.on_message)

    async def on_message(self, topic, payload):
        message = json.loads(payload.decode())

        self.logger.info(message["payload"].replace("\r", "\n").strip())

    async def run(self):
        self.logger.info("Starting plain terminal output")
        while True:
            await asyncio.sleep(1)
