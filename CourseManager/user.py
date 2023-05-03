from flask import jsonify,current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import EmailField, PasswordField, StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, email, name, password, avatar_path,role="member"):
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
    
    def has_role(self, role_name):
        return self.role == role_name
    def get_id(self):
        return self.email


class SignupForm(FlaskForm):
    email = EmailField('email',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    name = StringField('name',validators=[DataRequired()])
    avatar = FileField("avatar",validators=[FileAllowed(['jpg','png'])])

class LoginForm(FlaskForm):
    email = EmailField('email',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    remember_me = BooleanField('remember me', default=False)

class UpdateForm(FlaskForm):
    name = StringField('Name')
    avatar = FileField("Avatar",validators=[FileAllowed(['jpg','png'])])
    email = EmailField('Email')
    role = StringField('Role')
    password = PasswordField('Password')
    submit = SubmitField('Update')
    delete = SubmitField('Delete')