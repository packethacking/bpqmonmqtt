# BPQMON via MQTT

This project uses the MQTT output from LinBPQ to produce terminal output - as a replacement for monitoring traffic via QtTermTCP.

## MQTT Configuration

Provisioning and configuring an MQTT server is outside the scope of this document. I would recommend using [bpq-compose](https://github.com/packethacking/bpq-compose) to provision a complete 'BPQ Wrapper Stack'.

## BPQ Configuration

First, BPQ must be configured to output MQTT, add something like the following to `/etc/bpq32.cfg`

```text
MQTT=1
MQTT_HOSTNAME=localhost
MQTT_PORT=1883
MQTT_USERNAME=bpqmon
MQTT_PASSWORD=bpqmon
```

## Running this project

Once BPQ is successfully outputting MQTT traffic, there is a couple of ways to run this project.

```bash
poetry install
poetry run bpqmon --mqtt-hostname localhost --mqtt-port 1833 --mqtt-username bpqmon --mqtt-password bpqmon
```

There is also a docker image.

TODO: Fill in docker details once it is available
