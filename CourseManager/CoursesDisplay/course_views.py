from flask import Blueprint, abort, render_template, redirect, url_for, flash
from flask_login import current_user
import oracledb
from CourseManager.dbmanager import *

bp = Blueprint('course', __name__, url_prefix='/courses')

@bp.route('/domain/<domain_id>')
def display_courses(domain_id):
    try:
        courses = get_db().get_courses_from_domain(domain_id)
        if len(courses) == 0:
            abort(404)
        terms = []
        for course in courses:
            if course.term not in terms:
                terms.append(course.term)
        return render_template("courses.html", courses=courses, terms=terms, current_user=current_user)
    except oracledb.Error as e:
        flash("Something went wrong..")
        flash("Cannot reach the database")
        return redirect(url_for("home.index"))

@bp.route('/<course_id>')
def display_course(course_id):
    if get_db().get_course(course_id):
        return render_template("specific_course.html", course=get_db().get_course(course_id),current_user=current_user)
    abort(404)

@bp.route('/')
def choose_domain():
    try:
        domains = get_db().get_domains()
        return render_template("courses_home.html", domains=domains)
    except oracledb.Error as e:
        flash("Something went wrong..")
        flash("Cannot reach the database")
        return redirect(url_for("home.index"))
