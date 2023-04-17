from flask import Blueprint, render_template, redirect, url_for, flash
import oracledb
from CourseManager.dbmanager import *

bp = Blueprint('course', __name__, url_prefix='/courses')

@bp.route('/')
def display_courses():
    try:
        return render_template("courses.html", courses=get_db().get_courses(),
                               terms=get_db().get_terms(), domains=get_db().get_domains())
    except oracledb.Error as e:
        flash("Something went wrong..")
        flash("Cannot reach the database")
        return redirect(url_for("home.index"))

@bp.route('/<course_id>')
def display_course(course_id):
    if get_db().get_course(course_id):
        course = get_db().get_course(course_id)
        return render_template("specific_course.html", course=course,
                               domain=get_db().get_domain(course.domain_id),
                               term=get_db().get_term(course.term_id))
    flash(f"{course_id} course not found!")
    return redirect(url_for("course.display_courses"))