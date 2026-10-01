import azure.functions as func

from app.FlaskApp import flask_app

app = func.WsgiFunctionApp(
  app=flask_app.wsgi_app,
  http_auth_level=func.AuthLevel.FUNCTION
)