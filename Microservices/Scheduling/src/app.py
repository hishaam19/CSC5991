from flask import Flask

from api import scheduling

application = Flask(__name__)

application.config.from_mapping(
    SECRET_KEY='csc5991',
    SQLALCHEMY_DATABASE_URI="postgresql://okteto:okteto@10.152.137.106:5432/Scheduling",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_ECHO=True
)

application.register_blueprint(scheduling.bp)

from models import db
db.init_app(application)

@application.route("/", methods=['GET'])
def hello_world():
    return "<p>Candidate Service Running</p>"
