import hmac
import os

from flask import Flask, request, jsonify
from .inference import predict_mnist, predict_catsdogs, InvalidImage

MAX_IMAGE_BYTES = 10 * 1024 * 1024  # 10 MB por imagen
API_KEY = os.getenv("CS1_API_LAB_1", "")

flask_app = Flask(__name__)
# Tope de la petición completa: imagen + margen para las cabeceras multipart.
flask_app.config["MAX_CONTENT_LENGTH"] = MAX_IMAGE_BYTES + 512 * 1024

@flask_app.before_request
def _check_api_key():
    if request.path == "/health":
        return None
    sent = request.headers.get("x-api-key", "")
    if not API_KEY or not hmac.compare_digest(sent, API_KEY):
        return jsonify(error="API key inválida o ausente"), 401

@flask_app.errorhandler(413)
def _too_large(_):
    return jsonify(error="La imagen supera 10 MB"), 413

def _get_image():
    f = request.files.get("image")
    if f is None or f.filename == "":
        return None
    return f.stream

def _size(stream):
    stream.seek(0, os.SEEK_END)
    size = stream.tell()
    stream.seek(0)
    return size

def _run(predictor):
    stream = _get_image()
    if stream is None:
        return jsonify(error="Falta el campo 'image'"), 400
    if _size(stream) > MAX_IMAGE_BYTES:
        return jsonify(error="La imagen supera 10 MB"), 413
    try:
        return jsonify(predictor(stream))
    except InvalidImage:
        return jsonify(error="Imagen inválida"), 400

@flask_app.get("/health")
def health():
    return jsonify(status="ok")

@flask_app.post("/mnist")
def mnist():
    return _run(predict_mnist)

@flask_app.post("/catsdogs")
def catsdogs():
    return _run(predict_catsdogs)
