from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Scheduling(db.Model):
    __tablename__ = 'scheduling'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(USERNAME_LEN_MAX), nullable=False)
    email = db.Column(db.String(EMAIL_LEN_MAX), nullable=False)
    start_time = db.Column(db.Integer, nullable=False)
    end_time = db.Column(db.Integer, nullable=False)
    timezone = db.Column(db.String(TIMEZONE_LEN_MAX), nullable=False)
    yearsofexperience = db.Column(db.String(128))
    worklocation = db.Column(db.String(128))
    willingtorelocate = db.Column(db.Boolean)
    message = db.Column(db.String(MESSAGE_LEN_MAX), nullable=False)
