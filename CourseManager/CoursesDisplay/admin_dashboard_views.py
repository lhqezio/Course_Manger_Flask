from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
from ..dbmanager import get_db
from ..user import User, UpdateForm
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from .auth_views import add_avatar

bp = Blueprint('admin_dashboard', __name__, url_prefix='/admin_dashboard')

@bp.route('/', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    # Get all users from the database
    db = get_db()
    users = db.get_users()
    forms = []
    users = [user for user in users if (current_user.has_role('member') and user.role == 'member') or (current_user.has_role('admin_user_gp') and (user.role == 'member' or user.role == 'admin_user_gp')) or (current_user.has_role('admin'))]
    if current_user.has_role('admin_user_gp') or current_user.has_role('admin'):
        for user in users:
            form = UpdateForm()
            form.old_email.data = user.email
            forms.append(form)
    if request.method == 'POST':
        # Handle form submission
        form = [form for form in forms if form.old_email.data == request.form['old_email'] ][0]
        
        if form.validate_on_submit():
            if form.submit.data:
                old_email = form.old_email.data
                old_user = db.get_user(old_email)
                if not old_user:
                    flash('User not found.')
                    return redirect(url_for('.admin_dashboard'))
                email = form.email.data
                name = form.name.data
                role = form.role.data
                avatar = form.avatar.data
                password = form.password.data
                if not password and not email and not name and not role and not avatar:
                    flash("No change was made")
                    return redirect(url_for('.admin_dashboard',current_user=current_user, users=users, forms=forms))
                if not email:
                    email = old_email
                if not name:
                    name = old_user.name
                if not role:
                    role = old_user.role
                if not password:
                    password = old_user.password
                if not avatar:
                    avatar = old_user.avatar_path
                else:
                    add_avatar(avatar)
                new_user = User(email, name,password,avatar,role)
                # Update the user's name and role
                db.update_user(new_user, old_email)
                flash('User updated successfully.')
            elif form.delete.data:
                print("h")
            
            return redirect(url_for('.admin_dashboard',current_user=current_user, users=users, forms=forms))
    # Render the admin dashboard with the list of users
    return render_template('admin_dashboard.html',current_user=current_user, users=users, forms=forms)