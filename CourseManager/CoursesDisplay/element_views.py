from flask import Blueprint, render_template, redirect, url_for, flash, request
import oracledb
from CourseManager.dbmanager import *
from CourseManager.element import *
from flask_login import current_user

bp = Blueprint('element', __name__, url_prefix='/elements')

@bp.route('/')
def display_elements():
    try:
        return render_template("elements.html", elements=get_db().get_elems(),current_user = current_user)
    except oracledb.Error as e:
        flash("Something went wrong..")
        flash("Cannot reach the database")
        return redirect(url_for("home.index"))

@bp.route('/<element_id>')
def display_element(element_id):
    if get_db().get_element(element_id):
        element = get_db().get_element(element_id)
        return render_template("specific_element.html", element=element,current_user = current_user)
    flash(f"{element_id} element not found!")
    return redirect(url_for("element.display_elements"))

@bp.route('/new-element',methods=['GET','POST'])
def add_element():
    if get_db():
        db=get_db()
        form=ElementForm()
        dom_ids=[]
        domains=db.get_domains()
        for dom in domains:
            dom_ids.append((f'{dom.domain_id}',f'{dom.domain}'))
        form.competency_id.choices=dom_ids
        if request.method=="POST" and form.validate_on_submit():
            element_id=form.element_id.data
            element_order=form.element_order.data
            element=form.element.data
            element_criteria=form.element_criteria.data
            competency_id=form.competency_id.data
            element=Element(element_id,element_order,element,element_criteria,competency_id,0)
            try:
                db.add_element(element=element)
                flash("New element")
                return redirect(url_for("element.display_element",element_id=element_id))
            except:
                flash("Cannot add this element")
        return render_template("element_form.html",form=form)
    flash("DB connection fail")
    return redirect(url_for("element.display_elements"))

@bp.route('/edit-element/<element_id>',methods=['POST','GET'])
def edit_element(element_id):
    db=get_db()
    if db and db.get_element(element_id):
        element=db.get_element(element_id)
        form=ElementForm()
        dom_ids=[]
        for dom in db.get_domains():
            dom_ids.append((f'{dom.domain_id}',f'{dom.domain}'))
        form.competency_id.choices=dom_ids
        if request.method=="POST" and form.validate_on_submit():
            element_id=form.element_id.data
            element_order=form.element_order.data
            element=form.element.data
            element_criteria=form.element_criteria.data
            competency_id=form.competency_id.data
            element=Element(element_id,element_order,element,element_criteria,competency_id,0)
            try:
                db.update_element(element=element)
            except:
                flash("Cannot edit this element")
        return render_template("edit_element_form.html", element=element, form=form)
    flash("DB connection fail")
    return redirect(url_for("element.display_elements"))

@bp.route('/delete-element/<element_id>',methods=['POST','GET'])
def delete_element(element_id):
    db=get_db()
    if db and db.get_element(element_id):
        element=db.get_element(element_id)
        db.delete_element(element)
        flash("Element deleted ",f'{element.element}')
    return redirect(url_for("element.display_elements"))