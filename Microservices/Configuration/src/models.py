from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB

db = SQLAlchemy()
username = "okteto"
password = "okteto"
dbname = "Configuration"

class Configuration(db.Model):
    __tablename__ = 'configuration'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    configurationKey = db.Column(db.String(128), unique=True, nullable=False)
    configurationValue = db.Column(JSONB)