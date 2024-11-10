import asyncio

import paho.mqtt.client as mqtt
import structlog


class MQTTInput:
    def __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.logger = structlog.get_logger().bind(input="mqtt")

        self.listeners = []

    def on_connect(self, client, userdata, flags, reason_code, properties):
        self.logger.info(f"Connected with result code {reason_code}")

    def on_message(self, client, userdata, message):
        for listener in self.listeners:
            asyncio.run(listener(message.topic, message.payload))

    async def run(self):
        self.logger.info("Starting MQTT input")
        self.logger.info(
            f"Connecting to {self.hostname}:{self.port} as {self.username}"
        )

        mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqttc = mqttc
        self.mqttc.on_connect = self.on_connect
        self.mqttc.username_pw_set(self.username, self.password)
        self.mqttc.connect(self.hostname, self.port)

        self.mqttc.subscribe("PACKETNODE/ax25/trace/bpqformat/#")
        self.mqttc.on_message = self.on_message

        self.mqttc.loop_start()
        self.logger.info("MQTT Loop started")
        while True:
            await asyncio.sleep(1)
