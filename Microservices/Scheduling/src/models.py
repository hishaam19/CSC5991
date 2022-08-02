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

    def __repr__(self):
        return self.email

class Scheduling(db.Model):
    __tablename__ = 'scheduling'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company = db.relationship('User', foreign_keys=[company_id], backref=db.backref('company', lazy=True))
    client = db.relationship('User', foreign_keys=[client_id], backref=db.backref('client', lazy=True))

    def __repr__(self):
        return self.title

db.create_all()
