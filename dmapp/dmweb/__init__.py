import os

from flask import Flask
from dmweb import dm

def create_app(test_config=None):

    app = Flask("deskmeter") #instance_relative_config=True

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(dm.dmbp)

    return app


