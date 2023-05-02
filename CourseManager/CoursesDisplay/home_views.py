from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user
bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('index.html',current_user = current_user)