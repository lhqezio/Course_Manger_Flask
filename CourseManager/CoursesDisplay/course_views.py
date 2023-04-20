from flask import Blueprint, render_template, redirect, url_for, flash
import oracledb
from CourseManager.dbmanager import *
from CourseManager.course import Course,CourseForm

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
@bp.route('/editcourse/<course_id>')

@bp.route('/edit/<course_id>', methods=['POST'])
def edit_course(course_id):
    db=get_db()
    if db.get_course(course_id):
        course = db.get_course(course_id)
        form=CourseForm
        if request.method == 'POST':
            if form.validate_on_submit():
                course_number=form.course_number.data
                course_title=form.course_title.data
                theory_hours=form.theory_hours.data
                lab_hours=form.lab_hours.data
                homework_hours=form.homework_hours.data
                description=form.description.data
                domain_id=form.domain_id.data
                term_id=form.term_id.data
                course = Course(course_number, course_title,theory_hours,lab_hours,homework_hours,description,domain_id,term_id)
                try:
                    db.update_course(course=None)
                except:
                    flash('Course update DB Error')
            else:
                flash('Invalid input')
        return render_template("edit_course.html", course=course, form=form, terms=db.get_terms(), domains=db.get_domains())
    else:
        redirect(url_for('display_courses'))
    