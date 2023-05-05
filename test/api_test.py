import flask_unittest
from ..CourseManager.__init__ import create_app

class TestApi(flask_unittest.ClientTestCase):
    app = create_app()

    def test_get_courses(self, client):
        response = client.get("/api/courses/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"next_page": None, "prev_page": None, "courses": []})