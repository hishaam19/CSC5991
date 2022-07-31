from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Candidate(db.Model):
    __tablename__ = 'candidates'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    yearsofexperience = db.Column(db.String(128))
    worklocation = db.Column(db.String(128))
    willingtorelocate = db.Column(db.Boolean)
    phonenumber = db.Column(db.String(128))
    username = db.Column(db.String(128))

    def serialize(self):
        return {
            'id': self.id,
            'yearsofexperience': self.yearsofexperience,
            'worklocation': self.worklocation,
            'willingtorelocate': self.willingtorelocate,
            'phonenumber': self.phonenumber,
            'username': self.username
        }