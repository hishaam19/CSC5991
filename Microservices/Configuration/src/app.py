from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .api import configuration

application = Flask(__name__)

import models
application.register_blupring(configuration.bp)

@application.route("/", methods=['GET'])
def hello_world():
    return "<p>Configuration Running</p>"
