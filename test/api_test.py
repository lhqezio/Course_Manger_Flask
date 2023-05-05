
from CourseManager.__init__ import create_app
from CourseManager.course import Course
from CourseManager.domain import Domain
import flask_unittest
class TestApi(flask_unittest.ClientTestCase):
    app = create_app()
    SAMPLE_COURSE={
                "competencies": [
                "http://127.0.0.1:5000/api/competencies/00Q2/",
                "http://127.0.0.1:5000/api/competencies/00Q4/",
                "http://127.0.0.1:5000/api/competencies/00Q3/"
                ],
                "course_number": "420-110-TE",
                "course_title": "TEST",
                "description": "TEST",
                "domain": {
                "domain": "Programming, Data Structures, and Algorithms",
                "domain_description": "The courses in the Programming, Data Structures and Algorithms domain teach the knowledge and skills required to design and program solutions to typical information technology problems. The students are taught object-oriented programming in the context of standalone, event-driven and web-based programs.",
                "domain_id": 1
                },
                "homework_hours": 3,
                "lab_hours": 3,
                "term": {
                "term_id": 1,
                "term_name": "Fall"
                },
                "theory_hours": 3
                }

    def test_get_courses(self, client):
        response = client.get("/api/courses/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["next_page"], 'http://localhost/api/courses/?page=2')
        self.assertEqual(response.json["prev_page"], None)
        self.assertEqual(len(response.json["courses"]), 2)

    def test_get_courses_page_2(self, client):
        response = client.get("/api/courses/?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["next_page"], 'http://localhost/api/courses/?page=3')
        self.assertEqual(response.json["prev_page"], 'http://localhost/api/courses/?page=1')
        self.assertEqual(len(response.json["courses"]), 2)

    def test_insert_course(self, client):
        response = client.post("/api/courses/",json=(self.SAMPLE_COURSE))
        self.assertEqual(response.status_code, 200)
        response = client.get("/api/courses/")
        self.assertEqual(response.status_code, 200)


    def test_get_course(self,client):
        response = client.get("/api/courses/1/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["id"], 1)
        self.assertEqual(response.json["name"], "course1")
        self.assertEqual(response.json["description"], "description1")
        self.assertEqual(response.json["domain"], "domain1")
        self.assertEqual(response.json["credits"], 1)
        self.assertEqual(response.json["term_id"], 1)
        self.assertEqual(response.json["teacher_id"], 1)