from flask import jsonify
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import EmailField, PasswordField, StringField, BooleanField
from wtforms.validators import DataRequired
from flask_login import UserMixin, login_manager
from .dbmanager import get_db

class User(UserMixin):
    def __init__(self, email, name, password, avatar_path,role="User"):
        if not isinstance(email, str):
            raise TypeError()
        if not isinstance(password, str):
            raise TypeError()
        if not isinstance(name, str):
            raise TypeError()
        if avatar_path and not isinstance(avatar_path, str):
            raise TypeError()
        if not isinstance(role, str):
            raise TypeError()
        self.email = email
        self.password = password
        self.name = name
        self.avatar_path = avatar_path
        self.role = role
    
    def has_role(self, role):
        return self.role == role

class SignupForm(FlaskForm):
    email = EmailField('email',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    name = StringField('name',validators=[DataRequired()])
    avatar = FileField("avatar",validators=[FileAllowed(['jpg','png'])])

class LoginForm(FlaskForm):
    email = EmailField('email',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    remember_me = BooleanField('remember me', default=False)

@login_manager.user_loader
def load_user(email):
    return get_db().get_user(email)