
from CourseManager.__init__ import create_app
from CourseManager.course import Course
from CourseManager.domain import Domain
import flask_unittest
class TestApi(flask_unittest.ClientTestCase):
    app = create_app()
    SAMPLE_COURSE={
                "competencies": [
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
                "term_name": "Fall  "
                },
                "theory_hours": 3
                }
    SAMPLE_COURSE_UPDATE={
                "competencies": [
                ],
                "course_number": "420-110-TE",
                "course_title": "TEST UPDATE",
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
                "term_name": "Fall  "
                },
                "theory_hours": 3
                }
    SAMPLE_COMPETENCY= {
            "competency": "TEST",
            "competency_achievement": "* For problems that are easily solved * Using basic algorithms * Using a debugger and a functional test plan",
            "competency_id": "TEST",
            "competency_type": "Mandatory",
            "elements": [
            ]
        }
    SAMPLE_COMPETENCY_UPDATED= {
            "competency": "TEST_UPDATED",
            "competency_achievement": "* For problems that are easily solved * Using basic algorithms * Using a debugger and a functional test plan",
            "competency_id": "TEST",
            "competency_type": "Mandatory",
            "elements": [
            ]
        }
    SAMPLE_ELEMENT= {

                "competency_id": "TEST_UPDATED",
                "element": "TEST.",
                "element_criteria": "TEST",
                "element_id": 1,
                "element_order": 1,
                "hours": 1
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
        
    def test_get_course(self,client):
        response = client.get("/api/courses/420-440-DW/")
        self.assertEqual(response.status_code, 200)

    def test_get_course_404(self, client):
        response = client.get("/api/courses/420-110-TE/")
        self.assertEqual(response.status_code, 404)

    def test_update_course(self,client):
        response = client.put("/api/courses/420-110-TE/",json=(self.SAMPLE_COURSE_UPDATE))
        self.assertEqual(response.status_code, 200)
        response = client.get("/api/courses/420-110-TE/")
        self.assertEqual(response.json,self.SAMPLE_COURSE_UPDATE)

    def test_update_fail(self,client):
        response = client.put("/api/courses/420-110-TE/",json=({'junk':'junk'}))
        self.assertEqual(response.status_code, 400)
        

    def test_delete_course(self,client):
        response = client.delete("/api/courses/420-110-TE/")
        self.assertEqual(response.status_code, 200)
        response = client.get("/api/courses/420-110-TE/")
        self.assertEqual(response.status_code, 404)

    def test_delete_course_400(self,client):
        response = client.delete("/api/courses/FAIL/")
        self.assertEqual(response.status_code, 400)

    def test_get_competencies(self,client):
        response = client.get("/api/competencies/")
        self.assertEqual(response.status_code, 200)
    
    def test_get_competencies_fail(self,client):
        response = client.get("/api/competencies/FAIL")
        self.assertEqual(response.status_code, 308)

    def test_get_competency(self,client):
        response = client.get("/api/competencies/00Q2/")
        self.assertEqual(response.status_code, 200)
    
    def test_get_competency_fail(self,client):
        response = client.get("/api/competencies/FAIL/")
        self.assertEqual(response.status_code, 404)
    
    def test_add_competency(self,client):
        response = client.post("/api/competencies/",json=(self.SAMPLE_COMPETENCY))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,{"message": "Success"})

    def test_add_competency_fail(self,client):
        response = client.post("/api/competencies/",json=({'junk':'junk'}))
        self.assertEqual(response.status_code, 400)

    def test_update_competency(self,client):
        response = client.put("/api/competencies/TEST/",json=(self.SAMPLE_COMPETENCY_UPDATED))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,{"message": "Success"})

    def test_update_competency_fail(self,client):
        response = client.put("/api/competencies/TEST/",json=({'junk':'junk'}))
        self.assertEqual(response.status_code, 400)

    def test_get_elements_of_competency(self,client):
        response = client.get("/api/competencies/00Q2/elements/")
        self.assertEqual(response.status_code, 200)

    def test_get_elements_of_competency_fail(self,client):
        response = client.get("/api/competencies/FAIL/elements/")
        self.assertEqual(response.status_code, 404)
    
    def test_get_element_of_competency(self,client):
        response = client.get("/api/competencies/00Q2/elements/52/")
        self.assertEqual(response.status_code, 200)

    def test_get_element_of_competency_fail(self,client):
        response = client.get("/api/competencies/FAIL/elements/52/")
        self.assertEqual(response.status_code, 404)

    def test_add_element_to_competency(self,client):
        response = client.post("/api/competencies/TEST/elements/",json=(self.SAMPLE_ELEMENT))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,{"message": "Success"})

    def test_add_element_to_competency_fail(self,client):
        response = client.post("/api/competencies/TEST/elements/",json=({'junk':'junk'}))
        self.assertEqual(response.status_code, 400)

    def test_delete_competency(self,client):
        response = client.delete("/api/competencies/TEST/")
        self.assertEqual(response.status_code, 200)
        response = client.get("/api/competencies/TEST/")
        self.assertEqual(response.status_code, 404)

    def test_delete_competency_fail(self,client):
        response = client.delete("/api/competencies/FAIL/")
        self.assertEqual(response.status_code, 400)
    