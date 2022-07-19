from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB

from app import application

db = SQLAlchemy(application)
username = "okteto"
password = "okteto"
dbname = "Configuration"
application.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{username}:{password}@10.152.137.106:5432/{dbname}"

class Configuration(db.Model):
    __tablename__ = 'configuration'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    configurationKey = db.Column(db.String(128), unique=True, nullable=False)
    configurationValue = db.Column(JSONB)