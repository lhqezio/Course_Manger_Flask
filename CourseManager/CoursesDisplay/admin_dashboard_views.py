from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
from ..dbmanager import get_db
from ..user import User, UpdateForm
from flask_login import login_required, current_user
from flask_security import roles_required

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
            forms.append(UpdateForm(prefix=user.email))
    if request.method == 'POST':
        # Handle form submission
        form = request.form
        old_email = form['old_email']
        old_user = db.get_user(old_email)
        if not old_user:
            flash('User not found.')
            return redirect(url_for('.admin_dashboard'))
        email = form['email']
        name = form['name']
        role = form['role']
        avatar = form['avatar']
        if not email:
            email = old_email
        if not name:
            name = old_user.name
        if not role:
            role = old_user.role
        if not avatar:
            avatar = old_user.avatar
        new_user = User(email, name, role, avatar)
        # Update the user's name and role
        db.update_user(new_user, old_email)
        flash('User updated successfully.')
        return redirect(url_for('.admin_dashboard',current_user=current_user, users=users, forms=forms))
    # Render the admin dashboard with the list of users
    return render_template('admin_dashboard.html',current_user=current_user, users=users, forms=forms)