from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Mystudents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    degree = db.Column(db.String(100), nullable=False)
    institution_name = db.Column(db.String(255), nullable=False)
    passed_year = db.Column(db.Integer, nullable=False)
    degree_certificate = db.Column(db.String(255))
    id_proof = db.Column(db.String(255))

    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    conpassword = db.Column(db.String(100), nullable=False)

    status = db.Column(db.String(20), default="Pending")
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Mystudents {self.name}>"
