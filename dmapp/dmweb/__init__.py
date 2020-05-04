from flask import Flask
from dmweb import dm, dmcal

def create_app():

    app = Flask("deskmeter") 

    app.debug = True
    app.register_blueprint(dm.dmbp)

    return app


