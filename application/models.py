from application import db, login_manager
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin




class Post(db.model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	post = db.Column(db.String(250), nullable=False)
   
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return ''.join([
            'Date Posted: ', str(self.date_posted), '\r\n',
            'Post: ', self.post, '\r\n'
            'User: ', str(self.user_id)
        ])

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(60), nullable=False)
	last_name = db.Column(db.String(60), nullable=False)
	email = db.Column(db.String(150), nullable=False, unique=True)
	password = db.Column(db.String(200), nullable=False)
    image = db.column(db.String(100), nullable=False)
   	
    post = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return ''.join([
            'User ID: ', str(self.id), '\r\n',
            'Name: ', self.first_name, ' ', self.last_name, '\r\n',
            'Email: ', self.email
            'Image ID: ', self.image
        ])
