from flask import jsonify,current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import EmailField,HiddenField, PasswordField, StringField, BooleanField, SubmitField,SelectField
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
        print(role)
        if not ( role == 'member' or role == 'admin' or role == 'admin_gp_user' or role == 'blocked'):
            raise ValueError()
        self.email = email
        self.password = password
        self.name = name
        self.avatar_path = avatar_path
        self.role = role
    
    def has_role(self, role_name):
        return self.role == role_name
    def get_id(self):
        return self.email

ROLES = [('',''),('member','member'),('admin_gp_user','admin_gp_user'),('admin','admin'),('blocked','blocked')]
class SignupForm(FlaskForm):
    email = EmailField('email',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    name = StringField('name',validators=[DataRequired()])
    avatar = FileField("avatar")

class LoginForm(FlaskForm):
    email = EmailField('email',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    remember_me = BooleanField('remember me', default=False)

class UpdateForm(FlaskForm):
    name = StringField('Name',id=None)
    avatar = FileField("Avatar",id=None)
    email = EmailField('Email',id=None)
    role = SelectField(label="Role",id=None,choices=ROLES)
    password = PasswordField('Password',id=None)
    submit = SubmitField('Update',id=None)
    delete = SubmitField('Delete',id = None)
    old_email = HiddenField('old-email')