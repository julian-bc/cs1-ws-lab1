from flask import Flask, request, jsonify
from .models import get_model
from  .preprocess import prep_mnist, prep_catsdogs
import numpy as np

flask_app = Flask(__name__)
flask_app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB

def _get_image():
    f = request.files.get("image")
    if f is None or f.filename == "":
        return None
    return f.stream

@flask_app.post("/mnist")
def mnist():
    stream = _get_image()
    if stream is None:
        return jsonify(error="Falta el campo 'image'"), 400
    try:
        x = prep_mnist(stream)
    except Exception:
        return jsonify(error="Imagen inválida"), 400
    probs = get_model("mnist").predict(x, verbose=0)[0]
    
    return jsonify(
      digit=int(np.argmax(probs)), 
      confidence=float(np.max(probs))
    )

@flask_app.post("/catsdogs")
def catsdogs():
    stream = _get_image()
    if stream is None:
        return jsonify(error="Falta el campo 'image'"), 400
    try:
        x = prep_catsdogs(stream)
    except Exception:
        return jsonify(error="Imagen inválida"), 400
    p = get_model("catsdogs").predict(x, verbose=0)
    logit = float(p[0][0])
    score = 1.0 / (1.0 + np.exp(-logit))

    cat_pct = round(100 * (1 - score), 2)
    dog_pct = round(100 * score, 2)
    
    return jsonify(
      cat_percent=cat_pct,
      dog_percent=dog_pct,
      message=f"This image is {cat_pct:.2f}% cat and {dog_pct:.2f}% dog.",
    )