from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
from ..dbmanager import get_db
from ..user import User
from flask_login import login_required, current_user
from flask_security import roles_required

bp = Blueprint('admin_dashboard', __name__, url_prefix='/admin_dashboard')

@bp.route('/', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    # Get all users from the database
    db = get_db()
    users = db.get_users()
    users = [user for user in users if (current_user.has_role('member') and user.role == 'member') or (current_user.has_role('admin_user_gp') and (user.role == 'member' or user.role == 'admin_user_gp')) or (current_user.has_role('admin'))]
    print(current_user.role)
    if request.method == 'POST':
        # Handle form submission
        email = request.form['email']
        name = request.form['name']
        role = request.form['role']
        password = request.form['password']
        old_email = request.form['old_email']
        
        # Find the user in the database
        user = db.get_user(email).first()
        if not user:
            flash('User not found.')
            return redirect(url_for('.admin_dashboard'))
        
        # Update the user's name and role
        user = User(email, name, password, role)
        db.update_user(user, old_email)
        
        flash('User updated successfully.')
        return redirect(url_for('.admin_dashboard'))
    
    # Render the admin dashboard with the list of users
    return render_template('admin_dashboard.html',current_user=current_user, users=users)