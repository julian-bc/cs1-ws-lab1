"""MQTT publisher: sends an image and prints the prediction.

Run:  python publisher.py mnist digit.png
      python publisher.py catsdogs cat.jpg

Remote broker:
      MQTT_HOST=<dominio> python publisher.py catsdogs cat.jpg
"""

import os
import sys

import paho.mqtt.client as mqtt

BROKER = os.getenv("MQTT_HOST", "localhost")
PORT = int(os.getenv("MQTT_PORT", "1883"))
MAX_IMAGE_BYTES = 10 * 1024 * 1024
model, image_path = sys.argv[1], sys.argv[2]

if os.path.getsize(image_path) > MAX_IMAGE_BYTES:
    sys.exit("La imagen supera 10 MB")


def on_connect(client, userdata, flags, reason_code, properties):
    client.subscribe(f"cs1-api/{model}/response")  # listen first...
    with open(image_path, "rb") as f:
        client.publish(f"cs1-api/{model}", f.read())  # ...then send
    print(f"Image sent to cs1-api/{model}, waiting...")


def on_message(client, userdata, msg):
    print("Prediction:", msg.payload.decode())
    client.disconnect()


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT)
client.loop_forever()
