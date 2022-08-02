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
<<<<<<< HEAD
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
=======
            'fullName': self.fullname,
            'userName': self.username,
            'password': self.password,
            'email': self.email,
            'sessionId': self.sessionid,
            'role': self.role
        }

class Scheduling (db.Model):
    __tablename__ = 'scheduling'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullabl=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company = db.relationship('User', foreign_keys=[company_id], backref=db.backref('company', lazy=True))
    client = db.relationship('User', foreign_keys=[client_id], backref=db.backref('client', lazy=True))
>>>>>>> 6c5f7d004e094ad63eda33303ce2ec258edc0d04

    def serialize(self):
        return {
            'id': self.id,
<<<<<<< HEAD
            'interviewid': self.interviewid,
            'username': self.username
        }
=======
            'title': self.title,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'is_active': self.is_active,
            'company_id': self.company_id,
            'client_id': self.client_id,
            'company': self.company,
            'client': self.client            
        }

>>>>>>> 6c5f7d004e094ad63eda33303ce2ec258edc0d04
