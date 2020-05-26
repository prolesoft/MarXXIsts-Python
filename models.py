from os import listdir, path
from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class UserAccount(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    works = db.relationship("Document", back_populates="author")

    def __init__(self, dn, un, email, password):
        self.display_name = dn
        self.username = un
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User %r>" % self.username


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user_account.id'))
    author = db.relationship("UserAccount", back_populates="works")
    title = db.Column(db.String, unique=False, nullable=False)
    date_published = db.Column(db.DateTime, unique=False, nullable=False)
    path = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, author_id, title, path):
        self.author_id = author_id
        self.author = load_user(author_id)
        self.title = title
        self.path = path
        self.date_published = datetime.utcnow()
    
    def latest(self):
        """
        Returns path to latest version

        [::-1] reverses the sorted list of versions
        [:1] removes all elements but the first
        [0] extracts the first element
        """
        return path.join(self.path, sorted(listdir(self.path))[::-1][:1][0])



@login_manager.user_loader
def load_user(id):
    return UserAccount.query.get(int(id))
