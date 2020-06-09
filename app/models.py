from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5

@login.user_loader 
def load_user(id):
    return User.query.get(int(id))
class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64), index=True,unique=True)
    email = db.Column(db.String(120),index=True,unique=True)
    password_hash = db.Column(db.String(128))
    job = db.Column(db.String(64))
    company = db.Column(db.String(64))
    designation = db.Column(db.String(64))
    posts = db.relationship('Post',backref='author',lazy='dynamic')
    comment = db.relationship('Comment',backref='comment_by',lazy='dynamic')
    about_me = db.Column(db.String(140))
    facebook = db.Column(db.String(64))
    twitter = db.Column(db.String(64))
    linkedin = db.Column(db.String(64)) 
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest,size)

class Transaction(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    tr_id = db.Column(db.Integer)
    date = db.Column(db.String(64))
    description = db.Column(db.String(140))
    tr_type = db.Column(db.String(64))
    amount = db.Column(db.Integer)
    valid = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    comment = db.relationship('Comment',backref='comment_of',lazy='dynamic')
    document = db.relationship('Document',backref='document_of',lazy='dynamic')

    def __repr__(self):
        return '<Transaction {}>'.format(self.tr_id)        

class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    comment = db.Column(db.String(64))
    trans_id = db.Column(db.Integer,db.ForeignKey('transaction.id')) 
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Comment> {}>'.format(self.comment)

class Document(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    filename = db.Column(db.String(140))
    transaction_id = db.Column(db.Integer,db.ForeignKey('transaction.id'))

    def __repr__(self):
        return '<Document {}>'.format(self.body)     
     
class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
