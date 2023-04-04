# from flask import jsonify
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, BooleanField
# from wtforms.validators import DataRequired
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, email, name, password, avatarPath=None):
        if not isinstance(email, str):
            raise TypeError()
        if not isinstance(password, str):
            raise TypeError()
        if not isinstance(name, str):
            raise TypeError()
        if avatarPath and not isinstance(avatarPath, str):
            raise TypeError()
        self.email = email
        self.password = password
        self.name = name
        self.avatarPath = avatarPath

class SignupForm(FlaskForm):
    email = EmailField('email')
    password = PasswordField('password')
    name = StringField('name')

class LoginForm(FlaskForm):
    email = EmailField('email')
    password = PasswordField('password')
    remember_me = BooleanField('remember me')