from flask import Flask
import secrets
from CoursesDisplay.course_views import bp as course_views
from CoursesDisplay.competency_views import bp as competency_views

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY=secrets.token_urlsafe(32))
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    init_app(app)
    return app
def init_app(app):
    app.teardown_appcontext(cleanup)
    app.register_blueprint(course_views)
    app.register_blueprint(competency_views)
    with app.app_context():
        db = get_db()

def cleanup(value):
    close_db()
