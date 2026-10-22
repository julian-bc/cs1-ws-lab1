from flask import Flask, request, jsonify
from .inference import predict_mnist, predict_catsdogs, InvalidImage

flask_app = Flask(__name__)
flask_app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB

def _get_image():
    f = request.files.get("image")
    if f is None or f.filename == "":
        return None
    return f.stream

def _run(predictor):
    stream = _get_image()
    if stream is None:
        return jsonify(error="Falta el campo 'image'"), 400
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