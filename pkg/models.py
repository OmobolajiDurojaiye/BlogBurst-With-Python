from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db=SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    users_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    users_fname = db.Column(db.String(70), nullable=False)
    users_lname = db.Column(db.String(70), nullable=False)
    users_email = db.Column(db.String(50), nullable=False, unique=True)
    users_password = db.Column(db.String(255), nullable=False)
    users_date_of_birth = db.Column(db.Date, nullable=False)
    user_gender = db.Column(db.String(10))
    users_profile_pic = db.Column(db.String(225), nullable=True)

    posts = db.relationship('Post', backref='author')
    comments = db.relationship('Comment', backref='commenter')
    
    connections_as_user_one = db.relationship('Connection', backref='user_one_connection', foreign_keys='Connection.user_one')
    connections_as_user_two = db.relationship('Connection', backref='user_two_connection', foreign_keys='Connection.user_two')

    
    collaborations_as_writer_one = db.relationship('Collaboration', backref='writer_one_relationship', foreign_keys='Collaboration.writer_one')
    collaborations_as_writer_two = db.relationship('Collaboration', backref='writer_two_relationship', foreign_keys='Collaboration.writer_two')
    
    likes = db.relationship('Like', backref='liker')


class Post(db.Model):
    __tablename__ = 'posts'

    posts_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_writer = db.Column(db.Integer, db.ForeignKey('users.users_id'), nullable=False)
    posts_title = db.Column(db.String(120), nullable=False)
    posts_content = db.Column(db.Text, nullable=False)
    posts_likes = db.Column(db.Integer, nullable=False, default=0)
    posts_status = db.Column(db.Enum('Approved', 'Deleted', 'Drafted')) #, nullable=False
    posts_pic = db.Column(db.String(255)) #, nullable=False
    post_created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    post_updated_on = db.Column(db.DateTime(), default=datetime.utcnow)
    posts_description = db.Column(db.String(150), nullable=False)

    comments = db.relationship('Comment', backref='post')
    collaborations = db.relationship('Collaboration', backref='collaborated_post')
    likes = db.relationship('Like', backref='liked_post')


class Comment(db.Model):
    __tablename__ = 'comments'

    comments_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_commented_on = db.Column(db.Integer, db.ForeignKey('posts.posts_id'), nullable=False)
    user_commented = db.Column(db.Integer, db.ForeignKey('users.users_id'), nullable=False)
    comment_content = db.Column(db.Text, nullable=True)
    comment_made_on = db.Column(db.DateTime(), default=datetime.utcnow)
    user = db.relationship('User', foreign_keys='Comment.user_commented')


class Collaboration(db.Model):
    __tablename__ = 'collaborations'

    collaborations_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    collaborated_article_content = db.Column(db.Text, nullable=False)
    post_collaborated_on = db.Column(db.Integer, db.ForeignKey('posts.posts_id'), nullable=False)
    writer_one = db.Column(db.Integer, db.ForeignKey('users.users_id'), nullable=False)
    writer_two = db.Column(db.Integer, db.ForeignKey('users.users_id'), nullable=False)
    status = db.Column(db.Enum('pending', 'completed'), nullable=False)
    collab_date = db.Column(db.Date, nullable=False)


class Like(db.Model):
    __tablename__ = 'likes'

    like_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_liked = db.Column(db.Integer, db.ForeignKey('posts.posts_id'), nullable=False)
    like_date = db.Column(db.DateTime(), default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.users_id'), nullable=False)


class Admin(db.Model):
    __tablename__ = 'admin'

    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_username = db.Column(db.String(60), nullable=False)
    admin_password = db.Column(db.String(45), nullable=False)
    admin_last_login = db.Column(db.DateTime(), default=datetime.utcnow)


class Connection(db.Model):

    __tablename__ = 'connections'

    connections_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_one = db.Column(db.Integer, db.ForeignKey('users.users_id'), nullable=False)
    user_two = db.Column(db.Integer, db.ForeignKey('users.users_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)

    user_one_fk = db.ForeignKeyConstraint(['user_one'], ['users.users_id'])
    user_two_fk = db.ForeignKeyConstraint(['user_two'], ['users.users_id'])