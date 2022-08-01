from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(128))
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))
    email = db.Column(db.String(128))
    sessionid = db.Column(db.String(128))
    role = db.Column(db.String(128))

    def serialize(self):
        return {
            'id': self.id,
            'fullName': self.fullname,
            'userName': self.username,
            'password': self.password,
            'email': self.email,
            'sessionId': self.sessionid,
            'role': self.role
        }