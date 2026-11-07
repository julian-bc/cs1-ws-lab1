"""MQTT consumer: receives an image, asks the Flask API, publishes the answer.

Flow:  cs1-api/<model>  ->  POST {API_URL}/<model>  ->  cs1-api/<model>/response
Run:   python -m app.consumer   (with Mosquitto and the Flask app already running)
"""

import base64
import binascii
import os

import paho.mqtt.client as mqtt
import requests

BROKER = os.getenv("MQTT_HOST", "localhost")
PORT = int(os.getenv("MQTT_PORT", "1883"))
API = os.getenv("API_URL", "http://localhost:5000")
API_KEY = os.getenv("CS1_API_LAB_1", "")
MODELS = ["mnist", "catsdogs"]


def to_bytes(payload):
    """Raw image bytes (ESP32-CAM, publisher.py) or Base64 text (e.g. Postman)."""
    try:
        return base64.b64decode(payload, validate=True)
    except (binascii.Error, ValueError):
        return payload


def on_connect(client, userdata, flags, reason_code, properties):
    for model in MODELS:
        client.subscribe(f"cs1-api/{model}")
    print("Consumer ready, waiting for images...")


def on_message(client, userdata, msg):
    model = msg.topic.split("/")[1]  # cs1-api/<model>
    try:
        r = requests.post(
            f"{API}/{model}",
            files={"image": ("image", to_bytes(msg.payload))},
            headers={"x-api-key": API_KEY},
            timeout=30,
        )
        answer = r.text
    except requests.RequestException:
        answer = '{"error": "API not available"}'
    client.publish(f"cs1-api/{model}/response", answer)
    print(f"{msg.topic} ({len(msg.payload)} bytes) -> {answer.strip()}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT)
client.loop_forever()
