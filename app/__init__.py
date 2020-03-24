import os
from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config


def create_app(test_config=None):
    # create and configure the app
    _app = Flask(__name__)

    if test_config is None:
        _app.config.from_object(Config)
    else:
        _app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(_app.instance_path)
    except OSError:
        pass

    Bootstrap(_app)

    return _app


app = create_app()

from app import routes, errors
