from flask import Blueprint, abort, render_template, redirect, url_for, flash
from flask_login import current_user
import oracledb
from CourseManager.dbmanager import *

bp = Blueprint('competency', __name__, url_prefix='/competencies')

@bp.route('/')
def display_competencies():
    try:
        return render_template("competencies.html", competencies=get_db().get_competencies(),current_user=current_user)
    except oracledb.Error as e:
        flash("Something went wrong..")
        flash("Cannot reach the database")
        return redirect(url_for("home.index"))

@bp.route('/<competency_id>')
def display_competency(competency_id):
    if get_db().get_competency(competency_id):
        competency = get_db().get_competency(competency_id)
        return render_template("specific_competency.html", competency=competency,current_user =current_user)
    abort(404)