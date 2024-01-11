from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db=SQLAlchemy()

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    post_title = db.Column(db.String(255), nullable=False)
    post_image = db.Column(db.String(255))
    post_content = db.Column(db.Text(), nullable=False)
    post_description = db.Column(db.String(100), nullable=False)
    post_created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    post_updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow) 

    def __repr__(self):
        return f"<{self.post_title}:{self.post_content}>"
