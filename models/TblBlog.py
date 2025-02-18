from config import db

class Blog(db.Model):
    __tablename__ = 'TblBlog'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    image_path = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
