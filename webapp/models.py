from webapp import db
from sqlalchemy.ext.hybrid import hybrid_method
from datetime import datetime

from flask_migrate import Migrate


class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String, nullable=False)
    post_description = db.Column(db.String, nullable=False)

    def __init__(self, title, description):
        self.post_title = title
        self.post_description = description

    def __repr__(self):
        return '<title {}'.format(self.name)

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password_plaintext = db.Column(db.String, nullable=False)  # TEMPORARY - TO BE DELETED IN FAVOR OF HASHED PASSWORD
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, email, password_plaintext):
        self.email = email
        self.password_plaintext = password_plaintext
        self.authenticated = False

    @hybrid_method
    def is_correct_password(self, plaintext_password):
        return self.password_plaintext == plaintext_password

    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        """Requires use of Python 3"""
        return str(self.id)

    def __repr__(self):
        return '<User {0}>'.format(self.name)
