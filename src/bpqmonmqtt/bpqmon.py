import asyncio

import click

from .mqttconnectionhandler import MQTTInput
from .plain_terminal import PlainTerminal


async def start(fancy_terminal, plain_terminal, mqtt_details):
    if plain_terminal and fancy_terminal:
        raise ValueError("Cannot run in both plain and fancy terminal mode")

    tasks = []
    mqtt = MQTTInput(**mqtt_details)
    tasks.append(mqtt.run)

    if plain_terminal or (not fancy_terminal and not plain_terminal):
        plain = PlainTerminal(mqtt)
        tasks.append(plain.run)

    await asyncio.gather(*[task() for task in tasks])


@click.command()
@click.option(
    "--fancy-terminal", is_flag=True, default=False, help="Run in ~fancy~ terminal mode"
)
@click.option(
    "--plain-terminal", is_flag=True, default=False, help="Run in plain terminal mode"
)
@click.option("--mqtt-hostname", default="localhost", help="MQTT host to connect to")
@click.option("--mqtt-port", default=1883, help="MQTT port to connect to")
@click.option("--mqtt-username", default="", help="MQTT username")
@click.option("--mqtt-password", default="", help="MQTT password")
def run(
    fancy_terminal,
    plain_terminal,
    mqtt_hostname,
    mqtt_port,
    mqtt_username,
    mqtt_password,
):
    mqtt_details = {
        "hostname": mqtt_hostname,
        "port": mqtt_port,
        "username": mqtt_username,
        "password": mqtt_password,
    }

    # Get into asyncio world
    asyncio.run(start(fancy_terminal, plain_terminal, mqtt_details))


def run_wrapper():
    # Poetry entrypoint
    run(auto_envvar_prefix="BPQMON")


if __name__ == "__main__":
    run(auto_envvar_prefix="BPQMON")
