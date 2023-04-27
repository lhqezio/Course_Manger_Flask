from flask import Blueprint, render_template, redirect, url_for, flash, request, escape
import oracledb
from CourseManager.dbmanager import *
from CourseManager.competency import *

bp = Blueprint('competency', __name__, url_prefix='/competencies')

@bp.route('/')
def display_competencies():
    try:
        return render_template("competencies.html", competencies=get_db().get_competencies())
    except oracledb.Error as e:
        flash("Something went wrong..")
        flash("Cannot reach the database")
        return redirect(url_for("home.index"))

@bp.route('/<competency_id>')
def display_competency(competency_id):
    if get_db().get_competency(competency_id):
        competency = get_db().get_competency(competency_id)
        return render_template("specific_competency.html", competency=competency)
    flash(f"{competency_id} competency not found!")
    return redirect(url_for("competency.display_competencies"))

@bp.route('/edit/<competency_id>', methods=['POST','GET'])
def edit_competency(competency_id):
    competency_id=escape(competency_id)
    db=get_db()
    if db.get_competency(competency_id):
        competency = db.get_competency(competency_id)
        form=CompetencyForm()
        elements=[]
        for el in db.get_elems():
            elements.append((f'{el.element_id}',f'{el}'))
        form.elements.choices=elements
        if request.method == 'POST':
            if form.validate_on_submit():
                competency_id=form.competency_id.data
                competency=form.competency.data
                competency_achievement=form.competency_achievement.data
                competency_type=form.competency_type.data
                elements=[]
                for id_e in form.elements.data:
                    elements.append(db.get_element(int(id_e)))
                competency = Competency(competency_id, competency,competency_achievement,competency_type,elements)
                try:
                    db.update_competency(competency)
                    flash("updated")
                    return redirect(url_for('competency.display_competency'),competency_id=competency_id)
                except:
                    flash('Competency update DB Error')
            else:
                flash('Invalid input')
        return render_template("edit_competency.html", competency=competency, form=form)
    flash(f"{competency_id} competency not found!")
    return redirect(url_for("competency.display_competencies"))

@bp.route('/new-competency/', methods=['POST','GET'])
def add_competency():
    db=get_db()
    form=CompetencyForm()
    elements_list=[]
    for el in db.get_elems():
        elements_list.append((f'{el.element_id}',f'{el}'))
    form.elements.choices=elements_list
    if request.method == 'POST':
        if form.validate_on_submit():
            competency_id=form.competency_id.data
            competency=form.competency.data
            competency_achievement=form.competency_achievement.data
            competency_type=form.competency_type.data
            elements=[]
            for id_e in form.elements.data:
                 elements.append(db.get_element(id_e))
            competency = Competency(competency_id, competency,competency_achievement,competency_type,elements)
            try:
                db.add_competency(competency)
                db.commit()
                flash('Competency added')
                return redirect(url_for('competency.display_competency'),competency_id=competency_id)
            except:
                flash('Competency cannot be added')
        else:
            flash('Invalid input')
    return render_template("add_competency.html", form=form)
    