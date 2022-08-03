from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Availability(db.Model):
    __tablename__ = 'availability'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128))
    date = db.Column(db.Date)
    starttime = db.Column(db.Time)
    endtime = db.Column(db.Time)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'date': self.date,
            'starttime': self.starttime,
            'endtime': self.endtime
        }