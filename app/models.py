from email import message
import email
from email.mime import image
from app import login, db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api


@login.user_loader
def get_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    favorites = db.relationship('Admin', secondary='favorite')
    
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User|{self.username}>"

    def __str__(self):
        return self.username

cloudinary.config(
	cloud_name = os.environ.get('CLOUDINARYNAME'),
	api_key = os.environ.get('CLOUDINARY_API_KEY'),
	api_secret = os.environ.get('CLOUDINARY_API_SECRET'),
)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self): 
        return f"<Contact|id: {self.id}, email: {self.email}"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(100), nullable=False)
    post_content = db.Column(db.Text, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self): 
        return f"<Post|id: {self.id}, post_title: {self.post_title}"

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Favorites |id: {self.id}, Admin id:{self.admin_id}>"


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    shop_title = db.Column(db.String(100), nullable=False)
    posts = db.relationship('Post', backref='author')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self): 
        return f"<Contact|id: {self.id}, email: {self.email}"