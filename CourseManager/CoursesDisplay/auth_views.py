import os
from flask import Blueprint, current_app, flash, redirect, render_template, request, send_from_directory, url_for
from ..dbmanager import get_db
from ..user import LoginForm, SignupForm, User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required,current_user

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
                avatar_dir = os.path.join(current_app.config['IMAGE_PATH'], form.email.data)
                avatar_path = os.path.join(avatar_dir, 'avatar.png')
                if not os.path.exists(avatar_dir):
                    os.makedirs(avatar_dir)
                file.save(avatar_path)
                hash = generate_password_hash(form.password.data)
                user = User(form.email.data, hash, form.name.data)
                get_db().add_user(user)
        else:
            flash("invalid form")
    return render_template('signup.html', form=form, current_user = current_user)

@bp.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            #Check our user
            user = get_db().get_user(form.email.data)
            if user:
                #Check the password
                if check_password_hash(user.password, form.password.data):
                    #User can login
                    login_user(user, form.remember_me.data)
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
def show_avatar(email):
    path = os.path.join(current_app.config['IMAGE_PATH'], email)
    return send_from_directory(path, 'avatar.png')
