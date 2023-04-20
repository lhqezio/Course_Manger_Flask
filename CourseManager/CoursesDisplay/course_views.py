from flask import Blueprint, render_template, redirect, url_for, flash
import oracledb
from CourseManager.dbmanager import *

bp = Blueprint('course', __name__, url_prefix='/courses')

@bp.route('/domain/<domain_id>')
def display_courses(domain_id):
    try:
        courses = get_db().get_courses_from_domain(domain_id)
        terms = []
        for course in courses:
            if course.term not in terms:
                terms.append(course.term)
        return render_template("courses.html", courses=courses, terms=terms)
    except oracledb.Error as e:
        flash("Something went wrong..")
        flash("Cannot reach the database")
        return redirect(url_for("home.index"))

@bp.route('/<course_id>')
def display_course(course_id):
    if get_db().get_course(course_id):
        return render_template("specific_course.html", course=get_db().get_course(course_id))
    flash(f"{course_id} course not found!")
    return redirect(url_for("course.display_courses"))