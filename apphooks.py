from app import app
from rest_api.models import POSTGRES_DB


@app.before_request
def before_request():
    POSTGRES_DB.connect()


@app.after_request
def after_request(response):
    POSTGRES_DB.close()
    return response