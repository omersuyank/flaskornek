from config import db

class User(db.Model):
    __tablename__ = 'TblUser'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)
    photo_url = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
