from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB

db = SQLAlchemy()

class Configuration(db.Model):
    __tablename__ = 'configuration'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    configurationKey = db.Column(db.String(128), unique=True, nullable=False)
    configurationValue = db.Column(JSONB)

    def serialize(self):
        return {
            'id': self.id,
            'configurationKey': self.configurationKey,
            'configurationValue': self.configurationValue
        }