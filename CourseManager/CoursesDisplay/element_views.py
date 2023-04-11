from flask import Blueprint, render_template, redirect, url_for, flash
import oracledb
from CourseManager.dbmanager import *

bp = Blueprint('element', __name__, url_prefix='/elements')

@bp.route('/')
def display_elements():
    try:
        return render_template("elements.html", elements=get_db().get_elements())
    except oracledb.Error as e:
        flash("Something went wrong..")
        flash("Cannot reach the database")
        return redirect(url_for("home.index"))

@bp.route('/<element_id>')
def display_element(element_id):
    if get_db().get_element(element_id):
        element = get_db().get_element(element_id)
        return render_template("specific_element.html", element=element)
    flash(f"{element_id} element not found!")
    return redirect(url_for("element.display_elements"))