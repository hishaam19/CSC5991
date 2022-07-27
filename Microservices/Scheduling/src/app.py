from flask import Flask

application = Flask(__name__)

@application.route("/", methods=['GET'])
def hello_world():
    return "<p>Hello, World!</p>"
