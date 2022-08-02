from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Interview(db.Model):
    __tablename__ = 'interviews'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    durationinminutes = db.Column(db.Integer)
    recruiterusername = db.Column(db.String(128))
    candidateusername = db.Column(db.String(128))
    startdatetime = db.Column(db.TIMESTAMP)
    cancelled = db.Column(db.Boolean)

    def serialize(self):
        return {
            'id': self.id,
            'durationinminutes': self.durationinminutes,
            'recruiterusername': self.recruiterusername,
            'candidateusername': self.candidateusername,
            'startdatetime': self.startdatetime,
            'cancelled': self.cancelled
        }

class UserInterview(db.Model):
    __tablename__ = 'userinterviews'
    id = db.Column(db.Integer, primary_key=True)
    interviewid = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(128), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'interviewid': self.interviewid,
            'username': self.username
        }
