from flask import Blueprint, render_template, redirect, url_for, flash, request, escape
import oracledb
from CourseManager.dbmanager import *
from CourseManager.course import Course,CourseForm

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

@bp.route('/edit-course/<course_id>', methods=['POST'])
def edit_course(course_id):
    course_id=escape(course_id)
    db=get_db()
    if db.get_course(course_id):
        course = db.get_course(course_id)
        form=CourseForm()
        domains=[]
        for dom in db.get_domains():
            domains.append(f'{dom.domain_id}',f'{dom.domain}')
        terms=[]
        for term in db.get_terms():
            terms.append((f'{term.term_id}',f'{term.term_name}'))
        form.domain_id.choices=domains
        form.term_id.choices=terms
        if request.method == 'POST':
            if form.validate_on_submit():
                course_title=form.course_title.data
                theory_hours=form.theory_hours.data
                lab_hours=form.lab_hours.data
                homework_hours=form.homework_hours.data
                description=form.description.data
                domain_id=form.domain_id.data
                term_id=form.term_id.data
                course = Course(course_id, course_title,theory_hours,lab_hours,homework_hours,description,domain_id,term_id)
                try:
                    db.update_course(course)
                    redirect(url_for('display_course'),course_id=course_id)
                except:
                    flash('Course update DB Error')
            else:
                flash('Invalid input')
        return render_template("edit_course.html", course=course, form=form)
    else:
        flash('Course doesn\'t exist')
        redirect(url_for('display_courses'))

@bp.route('/add-course/', methods=['POST'])
def add_course():
    db=get_db()
    form=CourseForm()
    domains=[]
    for dom in db.get_domains():
        domains.append(f'{dom.domain_id}',f'{dom.domain}')
    terms=[]
    for term in db.get_terms():
        terms.append((f'{term.term_id}',f'{term.term_name}'))
    form.domain_id.choices=domains
    form.term_id.choices=terms
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
                db.add_course(course)
                redirect(url_for('display_course'),course_id=course_number)
            except:
                flash('Course cannot be added')
        else:
            flash('Invalid input')
    return render_template("add_course.html", course=course, form=form)
    