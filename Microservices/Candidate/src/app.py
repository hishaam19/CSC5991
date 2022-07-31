from flask import Flask

from api import candidate

application = Flask(__name__)

application.config.from_mapping(
    SECRET_KEY='csc5991',
    SQLALCHEMY_DATABASE_URI="postgresql://okteto:okteto@localhost:5432/Candidate",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_ECHO=True
)

application.register_blueprint(candidate.bp)

from models import db
db.init_app(application)

@application.route("/", methods=['GET'])
def hello_world():
    return "<p>Candidate Service Running</p>"
