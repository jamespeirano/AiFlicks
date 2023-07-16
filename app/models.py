# models.py
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(UserMixin, db.Document):
    meta = {'collection': 'users'}
    email = db.StringField(max_length=255, required=True, unique=True)
    password = db.StringField(required=True)
    is_admin = db.BooleanField(default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)