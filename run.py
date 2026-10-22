import os

from app.FlaskApp import flask_app
from app.models import get_model

if __name__ == "__main__":
  get_model("mnist")
  get_model("catsdogs")

  flask_app.run(
    host=os.getenv("FLASK_HOST", "0.0.0.0"),
    port=int(os.getenv("FLASK_PORT", "5000")),
    debug=False,
    use_reloader=False,
  )