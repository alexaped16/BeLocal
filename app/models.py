from email import message
import email
from email.mime import image
from app import login, db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os



@login.user_loader
def get_user(user_id):
    return User.query.get(user_id)

cloudinary.config(
	cloud_name = os.environ.get('CLOUDINARYNAME'),
	api_key = os.environ.get('CLOUDINARY_API_KEY'),
	api_secret = os.environ.get('CLOUDINARY_API_SECRET'),
)

# ASSOCIATION TABLE (FAVORITES TABLE)

user_shop = db.Table('user_shop', 

    db.Column('user_id', db.Integer, db.ForeignKey('user.id')), 
    db.Column('shop_id', db.Integer, db.ForeignKey('shop.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    favorites = db.relationship('Shop', secondary=user_shop, backref='user_favorites', lazy='select')
    contact_message = db.relationship('Contact', backref='author', lazy='dynamic')



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

    def add_favorite(self, shop):
        self.favorites.append(shop)
        db.session.commit()

    def remove_favorite(self, shop):
        self.favorites=[s for s in self.favorites if s != shop]
        db.session.commit()


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self): 
        return f"<Contact|id: {self.id}, email: {self.email}"



class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shop_title = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(100), nullable=False)
    url_for = db.Column(db.String(100), nullable=False)
    
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self): 
        return f"<Contact|id: {self.id}"



