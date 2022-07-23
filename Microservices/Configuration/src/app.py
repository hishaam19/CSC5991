from flask import Flask

from api import configuration

application = Flask(__name__)

username = "okteto"
password = "okteto"
dbname = "Configuration"
application.config.from_mapping(
    SECRET_KEY='csc5991',
    SQLALCHEMY_DATABASE_URI="postgresql://{username}:{password}@10.152.137.106:5432/{dbname}",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_ECHO=True
)

application.register_blueprint(configuration.bp)

from models import db
db.init_app(application)

@application.route("/", methods=['GET'])
def hello_world():
    return "<p>Configuration Running</p>"
