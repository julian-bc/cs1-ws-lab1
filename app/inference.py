import numpy as np
from .models import get_model
from .preprocess import prep_mnist, prep_catsdogs

class InvalidImage(Exception):
  pass

def predict_mnist(file_stream):
  try:
    x = prep_mnist(file_stream)
  except Exception as e:
    raise InvalidImage() from e
  probs = get_model("mnist").predict(x, verbose=0)[0]

  return {
    "digit": int(np.argmax(probs)),
    "confidence": float(np.max(probs)),
  }

def predict_catsdogs(file_stream):
  try:
    x = prep_catsdogs(file_stream)
  except Exception as e:
    raise InvalidImage() from e
  p = get_model("catsdogs").predict(x, verbose=0)
  logit = float(p[0][0])
  score = 1.0 / (1.0 + np.exp(-logit))

  cat_pct = round(100 * (1 - score), 2)
  dog_pct = round(100 * score, 2)

  return {
    "cat_percent": cat_pct,
    "dog_percent": dog_pct,
    "message": f"This image is {cat_pct:.2f}% cat and {dog_pct:.2f}% dog.",
  }

PREDICTORS = {
  "mnist": predict_mnist,
  "catsdogs": predict_catsdogs,
}