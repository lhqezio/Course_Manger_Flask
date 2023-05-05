import oracledb
from CourseManager.competency import Competency
from CourseManager.course import Course
from CourseManager.element import Element
from CourseManager.term import Term
from ..dbmanager import get_db
from flask import Blueprint, request, jsonify, abort, url_for

bp = Blueprint("courses_api", __name__, url_prefix="/api/")


@bp.route("/courses/", methods=["GET", "POST"])
def courses_api():
    if request.method == "POST":
        result = request.json
        print(result)
        if result:
            try:
                course = Course.from_json(result)
                get_db().add_course(course)
                return jsonify({"message": "Success"})
            except oracledb.DatabaseError:
                abort(409)
            except:
                abort(400)
            
        else:
            abort(400)
    else:
        page_num = 1
        if request.args:
            page = request.args.get("page")
            if page:
                page_num = int(page)
        courses, prev_page, next_page = get_db().get_courses_api(
            page_num=page_num, page_size=2
        )
        next_page_url = None
        prev_page_url = None
        if prev_page:
            prev_page_url = url_for("courses_api.courses_api", page=prev_page,_external=True)
        if next_page:
            next_page_url = url_for("courses_api.courses_api", page=next_page,_external=True)
        json_courses = {
            "next_page": next_page_url,
            "prev_page": prev_page_url,
            "courses": [course.to_dict() for course in courses]
        }
        return jsonify(json_courses)

@bp.route("courses/<course_id>/", methods=["GET", "PUT", "DELETE"])
def course_api(course_id):
    if request.method == "GET":
        course = get_db().get_course(course_id)
        if course:
            return jsonify(course.to_dict())
        else:
            abort(404)
    elif request.method == "PUT":
        result = request.json
        if result:
            try:
                course = Course.from_json(result)
                get_db().update_course(course)
            except oracledb.DatabaseError:
                abort(417)
            except:
                abort(400)
        else:
            abort(400)
    elif request.method == "DELETE":
        try:
            get_db().delete_course(course_id)
        except oracledb.DatabaseError:
            abort(400)
    return jsonify({"message": "Success"})

@bp.route("/competencies/", methods=["GET", "POST"])
def course_competencies_api():
    if request.method == "POST":
        result = request.json
        if result:
            try:
                competency = Competency.from_json(result)
                get_db().add_competency(competency)
            except oracledb.DatabaseError:
                abort(409)
            except:
                abort(400)
        else:
            abort(400)
    else:
        competencies = get_db().get_competencies()
        json_competencies = {
            "competencies": [competency.to_dict() for competency in competencies]
        }
    return jsonify(json_competencies)

@bp.route("/competencies/<competency_id>/", methods=["GET", "PUT", "DELETE"])
def course_competency_api(competency_id):
    if request.method == "GET":
        competency = get_db().get_competency(competency_id)
        if competency:
            return jsonify(competency.to_dict())
        else:
            abort(404)
    elif request.method == "PUT":
        result = request.json
        if result:
            try:
                competency = Competency.from_json(result)
                get_db().update_competency(competency)
            except oracledb.DatabaseError:
                abort(417)
            except:
                abort(400)
        else:
            abort(400)
    elif request.method == "DELETE":
        try:
            get_db().delete_competency(competency_id)
        except oracledb.DatabaseError:
            abort(400)
    return jsonify({"message": "Success"})

@bp.route("/competencies/<competency_id>/elements/", methods=["GET", "POST"])
def course_competency_elements_api(competency_id):
    if request.method == "POST":
        result = request.json
        if result:
            try:
                element = Element.from_json(result)
            except:
                abort(400)
            competency = get_db().get_competency(competency_id)
            for e in competency.elements:
                if e.id == element.id:
                    abort(400)
            competency.elements.append(element)
            try:
                get_db().update_competency(competency)
            except oracledb.DatabaseError:
                abort(409)
        else:
            abort(400)
    else:
        elements = get_db().get_elems_of_competency(competency_id)
    json_elements = {
        "elements": [element.__dict__ for element in elements]
    }
    return jsonify(json_elements)

@bp.route("competencies/<competency_id>/elements/<int:element_id>/", methods=["GET", "PUT", "DELETE"])
def course_competency_element_api(competency_id, element_id):
    if request.method == "GET":
        element = get_db().get_element(element_id)
        if element:
            return jsonify(element.__dict__)
        else:
            abort(404)
    elif request.method == "PUT":
        result = request.json
        if result:
            try:
                element = Element.from_json(result)
            except:
                abort(400)
            competency = get_db().get_competency(competency_id)
            for e in competency.elements:
                if e.element_id == element.element_id:
                    e = element
                    try:
                        get_db().update_competency(competency)
                    except oracledb.DatabaseError:
                        abort(409)
                    return jsonify({"message": "Success"})
            abort(400)
        else:
            abort(400)
    elif request.method == "DELETE":
        try:
            competency = get_db().get_competency(competency_id)
            for e in competency.elements:
                if e.element_id == element_id:
                    competency.elements.remove(e)
                    get_db().update_competency(competency)
                    return jsonify({"message": "Success"})
        except oracledb.DatabaseError:
            abort(400)
        abort(400)
    return jsonify({"message": "Success"})

@bp.route("/terms/", methods=["GET", "POST"])
def course_terms_api():
    if request.method == "POST":
        result = request.json
        if result:
            try:
                term = Term.from_json(result)
                get_db().add_term(term)
            except oracledb.DatabaseError:
                abort(409)
            except:
                abort(400)
        else:
            abort(400)
    else:
        terms = get_db().get_terms()
        json_terms = {
            "terms": [term.to_dict() for term in terms]
        }
    return jsonify(json_terms)

