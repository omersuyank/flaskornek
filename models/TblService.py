from config import db

class Service(db.Model):
    __tablename__ = 'TblService'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    service_code = db.Column(db.String(255), unique=True)
    is_active = db.Column(db.Boolean, default=True)
    short_description = db.Column(db.String(255))
    photo_url = db.Column(db.String(255))