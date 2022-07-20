from flask import Flask

from api import apiproxy

application = Flask(__name__)

application.register_blueprint(apiproxy.bp)

@application.route("/", methods=['GET'])
def hello_world():
    return "<p>Gatekeeper Running</p>"
