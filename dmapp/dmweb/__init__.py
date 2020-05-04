from flask import Flask
from dmweb import dm

def create_app():

    app = Flask("deskmeter") 

    app.register_blueprint(dm.dmbp)

    return app


