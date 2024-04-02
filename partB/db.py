from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Fan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255))
    brand = db.Column(db.String(255))
    fan_type = db.Column(db.String(255))


