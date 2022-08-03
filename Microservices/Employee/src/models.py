from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128))
    role = db.Column(db.String(128))
    hiredate = db.Column(db.Date)
    salary = db.Column(db.Integer)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'hiredate': self.hiredate,
            'salary': self.salary            
        }