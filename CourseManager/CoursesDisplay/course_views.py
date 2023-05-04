from flask import Blueprint, render_template, redirect, url_for, flash, request, escape
import oracledb
from CourseManager.dbmanager import get_db
from CourseManager.course import Course,CourseForm
from CourseManager.element import ElemHrsForm
from flask_login import current_user

bp = Blueprint('course', __name__, url_prefix='/courses')

@bp.route('/domain/<domain_id>')
def display_courses(domain_id):
    try:
        courses = get_db().get_courses_from_domain(domain_id)
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
    flash(f"{course_id} course not found!")
    return redirect(url_for("course.display_course"))

@bp.route('/edit-course/<course_id>', methods=['POST','GET'])
def edit_course(course_id):
    course_id=escape(course_id)
    db=get_db()
    if db.get_course(course_id):
        course = db.get_course(course_id)
        com_ids=[]
        for com in course.competencies:
            com_ids.append(com.competency_id)
        form=CourseForm(domain_id=course.domain.domain_id,term_id=course.term.term_id, description=course.description,competencies=com_ids)
        domains=[]
        for dom in db.get_domains():
            domains.append((f'{dom.domain_id}',f'{dom.domain}'))
        terms=[]
        for term in db.get_terms():
            terms.append((f'{term.term_id}',f'{term}'))
        competencies_list=[]
        for comp in db.get_competencies():
            competencies_list.append((f'{comp.competency_id}',f'{comp.competency}'))
        form.domain_id.choices=domains
        form.term_id.choices=terms
        form.competencies.choices=competencies_list
        
        if request.method == 'POST':
            if form.validate_on_submit():
                course_title=form.course_title.data
                theory_hours=form.theory_hours.data
                lab_hours=form.lab_hours.data
                homework_hours=form.homework_hours.data
                description=form.description.data
                domain=db.get_domain(form.domain_id.data)
                term=db.get_term(form.term_id.data)
                competencies=[]
                for com_id in form.competencies.data:
                    competencies.append(db.get_competency(com_id))
                course = Course(course_id, course_title,theory_hours,lab_hours,homework_hours,description,domain,term, competencies)
                try:
                    db.update_course(course)
                    db.commit()
                    return redirect(url_for('course.display_course',course_id=course_id))
                except:
                    flash('Course update DB Error, try again')
            else:
                flash('Invalid input')
        return render_template("edit_course.html", course=course, form=form)
    else:
        flash('Course doesn\'t exist')
        return redirect(url_for('course.display_courses'))

@bp.route('/new-course/', methods=['POST','GET'])
def add_course():
    db=get_db()
    form=CourseForm()
    domains=[]
    for dom in db.get_domains():
        domains.append((f'{dom.domain_id}',f'{dom.domain}'))
    terms=[]
    for term in db.get_terms():
        terms.append((f'{term.term_id}',f'{term}'))
    competencies_list=[]
    for comp in db.get_competencies():
        competencies_list.append((f'{comp.competency_id}',f'{comp.competency}'))
    form.domain_id.choices=domains
    form.term_id.choices=terms
    form.competencies.choices=competencies_list
    if request.method == 'POST':
        if form.validate_on_submit():
            course_id=form.course_number.data
            course_title=form.course_title.data
            theory_hours=form.theory_hours.data
            lab_hours=form.lab_hours.data
            homework_hours=form.homework_hours.data
            description=form.description.data
            domain=db.get_domain(form.domain_id.data)
            term=db.get_term(form.term_id.data)
            competencies=[]
            for com_id in form.competencies.data:
                competencies.append(db.get_competency(com_id))
            course = Course(course_id, course_title,theory_hours,lab_hours,homework_hours,description,domain,term,competencies)
            try:
                db.add_course(course)
                flash("New course added")
                db.commit()
                return redirect(url_for('course.display_course',course_id=course_id))
            except:
                flash('Course cannot be added')
        else:
            flash('Invalid input')
    return render_template("add_course.html", form=form)
    
@bp.route('/test/<course_id>', methods=['POST','GET'])
def elemenstHours(course_id):
    course_id=escape(course_id)
    db=get_db()
    if db.get_course(course_id):
        course = db.get_course(course_id)
        forms=[]
        competencies=course.competencies
        course_current_elemhrs=db.get_competency_elemhrs_from_course(course.course_number)
        for comp in competencies:
            form=ElemHrsForm()
            form.competency.label=comp.competency
            for elem in comp.elements:
                form.elem_hours.append_entry()
                x=form.elem_hours.last_index
                form.elem_hours.entries[x].course_element.data=elem.element
                if(elem in course_current_elemhrs):
                    y=course_current_elemhrs.index(elem)
                    elem.hours=course_current_elemhrs[y].hours
                form.elem_hours.entries[x].hours.data=elem.hours
            forms.append(form)
        if request.method == 'POST':
            if form.validate_on_submit():
                #db.update_course_elem_hrs(course)
                flash("DB course elem teaching hours set")
            else:
                flash("DB error")
    else: 
        flash("Invalid course id")
        return redirect(url_for('course.display_courses'))
    return render_template("course_elems_hrs.html", forms=forms, name=course.course_title)