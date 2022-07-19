from flask import Flask

from api import configuration

application = Flask(__name__)

import models
application.register_blueprint(configuration.bp)

@application.route("/", methods=['GET'])
def hello_world():
    return "<p>Configuration Running</p>"
