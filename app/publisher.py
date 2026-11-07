"""MQTT publisher: sends an image and prints the prediction.

Run:  python publisher.py mnist digit.png
      python publisher.py catsdogs cat.jpg
"""
import sys

import paho.mqtt.client as mqtt

BROKER = "localhost"
model, image_path = sys.argv[1], sys.argv[2]


def on_connect(client, userdata, flags, reason_code, properties):
  client.subscribe(f"cs1/{model}/response")  # listen first...
  with open(image_path, "rb") as f:
    client.publish(f"cs1/{model}/request", f.read())  # ...then send
  print(f"Image sent to cs1/{model}/request, waiting...")


def on_message(client, userdata, msg):
  print("Prediction:", msg.payload.decode())
  client.disconnect()


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, 1883)
client.loop_forever()