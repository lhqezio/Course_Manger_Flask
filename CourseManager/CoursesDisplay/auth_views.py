import os
from flask import Blueprint, current_app, flash, redirect, render_template, request, send_from_directory, url_for
from ..dbmanager import get_db
from ..user import LoginForm, SignupForm, User
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.datastructures import FileStorage
from flask_login import login_user, logout_user, login_required,current_user,login_user,login_manager

bp = Blueprint('auth', __name__, url_prefix='/auth/')

@bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if get_db().get_user(form.email.data):
                flash("User already exists")
            else:
                file = form.avatar.data
                fp = None
                if not file:
                    default_image = os.path.join(current_app.root_path,"Image", 'avatar.png')
                    fp = open(default_image,"rb")
                    file = FileStorage(fp)
                avatar_path = get_avatar_path(file,form.email.data)
                if fp:
                    fp.close()
                hash = generate_password_hash(form.password.data)
                user = User(form.email.data,form.name.data,hash,avatar_path)
                get_db().add_user(user)
                flash("User created")
        else:
            flash("invalid form")
    return render_template('signup.html', form=form, current_user = current_user)

@bp.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            #Check our user
            try:
                user = get_db().get_user(form.email.data)
            except ValueError:
                flash("Something wrong with your account, please contact the admin")
                user = None
            if user and user.role != 'blocked':
                #Check the password
                if check_password_hash(user.password, form.password.data):
                    #User can login
                    login_user(user, form.remember_me.data)
                    flash("Logged in successfully")
                    return redirect(url_for('course.choose_domain'))
                else:
                    flash("Cannot login")
            else:
                flash("Cannot login")
        else:
            flash("Cannot login")
    return render_template('login.html', form=form, current_user = current_user)
@bp.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/avatars/<email>/avatar.png')
@login_required
def show_avatar(email):
    path = os.path.join(current_app.config['IMAGE_PATH'], email)
    if not os.path.exists(path):
        path = os.path.join(current_app.root_path,"Image")
    return send_from_directory(path, 'avatar.png')

def get_avatar_path(file,email):
    avatar_dir = os.path.join(current_app.config['IMAGE_PATH'], email)
    avatar_path = os.path.join(avatar_dir, 'avatar.png')
    if not os.path.exists(avatar_dir):
        os.makedirs(avatar_dir)
    file.save(avatar_path)
    return avatar_path

def remove_avatar(email,new_email = None):
    avatar_dir = os.path.join(current_app.config['IMAGE_PATH'], email)
    if os.path.exists(avatar_dir):
        if new_email:
            new_avatar_dir = os.path.join(current_app.config['IMAGE_PATH'], new_email)
            os.rename(avatar_dir,new_avatar_dir)
        else:
            os.rmdir(avatar_dir)
