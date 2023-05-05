from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import current_user, login_required
from CourseManager.CoursesDisplay.auth_views import get_avatar_path

from CourseManager.dbmanager import get_db
from CourseManager.user import UpdateForm, User
bp = Blueprint('profile', __name__, url_prefix='/profile')
from werkzeug.security import generate_password_hash

@bp.route('/',methods=['GET','POST'])
@login_required
def profile():
    db = get_db()
    form = UpdateForm()
    form.old_email.data = current_user.email
    if request.method == 'POST':
        if form.validate_on_submit():
            old_email = form.old_email.data
            old_user = current_user
            if not old_user:
                flash('User not found.')
                return redirect(url_for('.profile'))
            email = form.email.data
            name = form.name.data
            avatar = form.avatar.data
            password = form.password.data
            if not password and not email and not name and not avatar:
                flash("No change was made")
                return redirect(url_for('.profile',current_user=current_user, form=form))
            if not email:
                email = old_email
            if not name:
                name = old_user.name
            if not password:
                password = old_user.password
            else:
                password = generate_password_hash(password)
            if not avatar:
                avatar_path = old_user.avatar_path
            else:
                get_avatar_path(avatar,old_email)
            role = old_user.role
            user = User(email,name,password,avatar_path,role)
            db.update_user(user)
            flash("Update successfully")
        else:
            flash("Invalid form")
    return render_template('profile.html',current_user=current_user, form=form)