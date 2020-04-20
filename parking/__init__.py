import os
from flask import Flask
from flask_bootstrap import Bootstrap
from parking.config import Config

bootstrap = Bootstrap()


def create_app(config_class=Config):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    bootstrap.init_app(app)
    with app.app_context():
        from parking import routes, errors

    return app

