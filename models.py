from app import db

class UserAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, dn, un, email):
        self.display_name = dn
        self.username = un
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username