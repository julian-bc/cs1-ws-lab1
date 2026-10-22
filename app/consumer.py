"""MQTT consumer: receives an image, asks the Flask API, publishes the answer.

Flow:  cs1/<model>/request  ->  POST http://localhost:5000/<model>  ->  cs1/<model>/response
Run:   python consumer.py   (with Mosquitto and the Flask app already running)
"""
import paho.mqtt.client as mqtt
import requests

BROKER = "localhost"
API = "http://localhost:5000"
MODELS = ["mnist", "catsdogs"]


def on_connect(client, userdata, flags, reason_code, properties):
  for model in MODELS:
    client.subscribe(f"cs1/{model}/request")
  print("Consumer ready, waiting for images...")


def on_message(client, userdata, msg):
  model = msg.topic.split("/")[1]  # cs1/<model>/request
  try:
    r = requests.post(f"{API}/{model}", files={"image": ("image", msg.payload)}, timeout=30)
    answer = r.text
  except requests.RequestException:
    answer = '{"error": "API not available"}'
  client.publish(f"cs1/{model}/response", answer)
  print(f"{msg.topic} ({len(msg.payload)} bytes) -> {answer.strip()}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, 1883)
client.loop_forever()