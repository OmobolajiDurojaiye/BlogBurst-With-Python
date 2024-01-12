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

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer(), primary_key=True)
    user_fname = db.Column(db.String(50), nullable=False)
    user_lname = db.Column(db.String(50), nullable=False)
    user_email = db.Column(db.String(100), unique=True, nullable=False)
    user_password = db.Column(db.String(255), nullable=False)
    user_date_of_birth = db.Column(db.Date())
    user_gender = db.Column(db.String(10))
    user_profile_pic = db.Column(db.String(255))

    def __repr__(self):
        return f"<{self.user_fname} {self.user_lname}>"
