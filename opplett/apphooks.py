from app import app
from opplett.models import POSTGRES_DB

"""
All methods to be called by the app itself.
This includes error and before/after handlers.
"""


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