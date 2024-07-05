from .extensions import db
from flask_login import UserMixin
# Define the User model
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120),nullable=False)
    password = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(10),  nullable=False)
    
    def get_id(self):
        return self.username # Return the username 

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    def __init__(self, username, password,email,phone,first_name,last_name):
        self.username = username
        self.email = email
        self.phone=phone
        self.first_name=first_name
        self.last_name=last_name
        self.set_password(password)  # Set the password using the set_password method

    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        return self.password, password