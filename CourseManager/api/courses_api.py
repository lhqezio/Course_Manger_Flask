from CourseManager.course import Course
from ..dbmanager import get_db
from flask import Blueprint, request, jsonify, abort, url_for

bp = Blueprint("courses_api", __name__, url_prefix="/api/courses/")


@bp.route("", methods=["GET", "POST"])
def courses_api():
    if request.method == "POST":
        result = request.json()
        if result:
            course = Course.from_json(result)
            get_db().add_course(course)
        else:
            abort(400)
    else:
        page_num = 1
        if request.args:
            page = request.args.get("page")
            if page:
                page_num = int(page)
        courses, prev_page, next_page = get_db().get_courses_api(
            page_num=page_num, page_size=10
        )
    next_page_url = None
    prev_page_url = None
    if prev_page:
        prev_page_url = url_for("courses_api.courses_api", page=prev_page)
    if next_page:
        next_page_url = url_for("courses_api.courses_api", page=next_page)
    json_courses = {
        "next_page": next_page_url,
        "prev_page": prev_page_url,
        "results": [course.to_dict() for course in courses],
    }
    return jsonify(json_courses)
