from flask import Blueprint

dmbp = Blueprint("deskmeter", __name__, url_prefix="/")

@dmbp.route("/")
def index():
    return "Hello, World!"
