from flask import Flask

@application.route("/", methods=['GET'])
def hello_world():
    return "<p>-</p>"
