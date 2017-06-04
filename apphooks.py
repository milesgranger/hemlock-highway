from app import app
from rest_api.models import POSTGRES_DB


@app.before_request
def before_request():
    """
    Open connections
    """
    POSTGRES_DB.connect()


@app.after_request
def after_request(response):
    """
    Close connections
    """
    POSTGRES_DB.close()
    return response