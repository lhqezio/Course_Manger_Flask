import os
import oracledb
from CourseManager.course import Course
from CourseManager.competency import Competency

class Database:
    def __init__(self):
        self.__user = os.environ['DBUSER']
        self.__password = os.environ['DBPWD']
        self.__host = '198.168.52.211'
        self.__port = 1521
        self.__service_name = 'pdbora19c.dawsoncollege.qc.ca'
        self.__conn = oracledb.connect(user = self.__user,
        password = self.__password, 
        host=self.__host, port=self.__port, 
        service_name = self.__service_name)
        self.__conn.autocommit = True

    def run_file(self, file_path):
        statement_parts = []
        with self.__conn.cursor() as cursor:
            with open(file_path, 'r') as f:
                for line in f:
                    statement_parts.append(line)
                    if line.strip('\n').strip('\n\r').strip().endswith(';'):
                        statement = "".join(
                            statement_parts).strip().rstrip(';')
                        if statement:
                            try:
                                cursor.execute(statement)
                            except Exception as e:
                                print(e)
                        statement_parts = []

    def close(self):
        if self.__conn:
            self.__conn.close()
            self.__conn = None

    def __get_cursor(self):
            for i in range(3):
                try:
                    return self.__conn.cursor()
                except Exception as e:
                    # Might need to reconnect
                    self.__reconnect()

    def __reconnect(self):
        try:
            self.close()
        except oracledb.Error as f:
            pass
        self.__conn = self.__connect()
    
    def __connect(self):
        return oracledb.connect(user=os.environ['DBUSER'], password=os.environ['DBPWD'],
                                host="198.168.52.211", port=1521, service_name="pdbora19c.dawsoncollege.qc.ca")


    def get_domains(self):
        domains = []
        with self.__get_cursor() as cursor:
            results = cursor.execute('select domain_id, domain, description from domains')
            for row in results:
                domain = Domain(domain=row[1],
                    description=row[2])
                domain.id = row[0]
                domains.append(domain)
        return domains

    def get_terms(self):
        terms = []
        with self.__get_cursor() as cursor:
            results = cursor.execute('select term_id, term_name from terms')
            for row in results:
                term = Term(id=row[0],domain=row[1],
                    description=row[2])
                terms.append(term)
        return terms
    
    def get_course(self,course_id):
        if not isinstance(course_id, str):
            raise TypeError()
        with self.__get_cursor() as cursor:
            results = cursor.execute('SELECT COURSE_ID, COURSE_TITLE, THEORY_HOURS, LAB_HOURS, WORK_HOURS, DESCRIPTION, DOMAIN_ID,TERM_ID FROM COURSES WHERE COURSE_ID LIKE :course_id',course_id=course_id)
            if results.rowcount != 1:
                raise oracledb.Error
            for row in results:
                course = Course()
        return course
    def get_courses_from_domain(self,domain_id):
        if not isinstance(domain_id, str):
            raise TypeError()
        courses = []
        with self.__get_cursor() as cursor:
            results = cursor.execute('SELECT COURSE_ID, COURSE_TITLE, THEORY_HOURS, LAB_HOURS, WORK_HOURS, DESCRIPTION, DOMAIN_ID,TERM_ID FROM COURSES')
            for row in results:
                course = Course()
                courses.append(course)
        return courses
    def get_courses_from_term(self,term_id):
        if not isinstance(term_id, str):
            raise TypeError()
        courses = []
        with self.__get_cursor() as cursor:
            results = cursor.execute('SELECT COURSE_ID, COURSE_TITLE, THEORY_HOURS, LAB_HOURS, WORK_HOURS, DESCRIPTION, DOMAIN_ID,TERM_ID FROM COURSES WHERE TERM_ID LIKE :term_id',term_id = term_id)
            for row in results:
                course = Course()
                courses.append(course)
        return courses
    
    def get_courses_from_domain(self,domain_id):
        if not isinstance(domain_id, str):
            raise TypeError()
        courses = []
        with self.__get_cursor() as cursor:
            results = cursor.execute('SELECT COURSE_ID, COURSE_TITLE, THEORY_HOURS, LAB_HOURS, WORK_HOURS, DESCRIPTION, DOMAIN_ID,TERM_ID FROM COURSES WHERE DOMAIN_ID LIKE :domain_id',domain_id = domain_id)
            for row in results:
                course = Course()
                courses.append(course)
        return courses
        

    def get_competencies(self):
        competencies = [] 
        with self.__get_cursor() as cursor:
            results = cursor.execute('select competency_id, competency, competency_achievement, competency_type from competencies')
            for row in results:
                competency = Competency(row[0],row[1],row[2],row[3])
                competencies.append(competency)
        return competencies

    def get_competencies_from_courses(self,course_id):
        if not isinstance(course_id, str):
            raise TypeError()
        course_competencies = [] 
        with self.__get_cursor() as cursor:
            results = cursor.execute('select competency_id, competency, competency_achievement, competency_type from view_courses_elements_competencies where course_id=:id',id=course_id)
            for row in results:
                competency = Competency(row[0],row[1],row[2],row[3])
                course_competencies.append(competency)
        return course_competencies

    def get_elems(self):
        elements = [] 
        with self.__get_cursor() as cursor:
            results = cursor.execute('select element_id, element_order, element, element_criteria, competency_id from elements')
            for row in results:
                element = Element(row[0],row[1],row[2],row[3],row[4])
                elements.append(element)
        return elements

    def get_elems_from_competency(self,comp_id):
        if not isinstance(comp_id, str):
            raise TypeError()
        competency_elems = [] 
        with self.__get_cursor() as cursor:
            results = cursor.execute('select element_id, element_order, element, element_criteria, competency_id from view_competencies_elements where competency_id=:id',id=comp_id)
            for row in results:
                element = Element(row[0],row[1],row[2],row[3],row[4])
                competency_elems.append(element)
        return competency_elems
    
    def get_elems_from_course(self,course_id):
        if not isinstance(course_id, str):
            raise TypeError()
        course_elems = []
        with self.__get_cursor() as cursor:
            results = cursor.execute('select element_id, element_order, element, element_criteria, competency_id from view_courses_elements_competencies where course_id=:id',id=course_id)
            for row in results:
                element = Element(row[0],row[1],row[2],row[3],row[4])
                course_elems.append(element)
        return course_elems
    
    def get_competency(self,competency_id):
        if not isinstance(competency_id, str):
            raise TypeError()
        with self.__get_cursor() as cursor:
            results = cursor.execute('select competency_id,competency,competency_achievement,competency_type from xompetencies where competency_id = :id',id=competency_id)
            if results.rowcount != 1:
                raise oracledb.Error
            for row in results:
                competency = Competency(row[0],row[1],row[2],row[3])
                return competency

    def add_course(self,course=None):
        if not isinstance(course, Course):
            raise TypeError()
        with self.__get_cursor() as cursor:
            cursor.execute('insert into courses values(:id,:title,:thrs,:lhrs,:hhrs,:descr,:dom_id,:term_id)',
                            id=course.course_number,title=course.course_title,thrs=course.theory_hours,lhrs=course.lab_hours,
                            hhrs=course.homework_hours,descr=course.description,dom_id=course.domain_id,term_id=course.term_id)

    def update_course(self,course=None):
        if not isinstance(course, Course):
            raise TypeError()
        with self.__get_cursor() as cursor:
            cursor.execute('update courses set course_title=:title,theory_hours=:thrs,lab_hours=:lhrs,homework_hours=:hhrs,description=:descr,domain_id=:dom_id,term_id=:term_id WHERE course_id=:id',
                            id=course.course_number,title=course.course_title,thrs=course.theory_hours,lhrs=course.lab_hours,
                            hhrs=course.homework_hours,descr=course.description,dom_id=course.domain_id,term_id=course.term_id)
                            
    def delete_course(self,course=None):
        if not isinstance(course, Course):
            raise TypeError()
        with self.__get_cursor() as cursor:
            cursor.execute('delete from courses where course_id=:id',id=course.course_number)

    def add_competency(self,competency=None):
        if not isinstance(competency, Competency):
            raise TypeError()
        with self.__get_cursor() as cursor:
            cursor.execute('insert into competencies values(:id,:name,:achievement,:type)',
                            id=competency.competency_id,name=competency.competency,
                            achievement=competency.competency_achievement,type=competency.competency_type)

    def update_competency(self,competency=None):
        if not isinstance(competency, Competency):
            raise TypeError()
        with self.__get_cursor() as cursor:
            cursor.execute('update competencies set competency=:name,competency_achievement=:achievement,competency_type=:type WHERE competency_id=:id',
                            id=competency.competency_id,name=competency.competency,
                            achievement=competency.competency_achievement,type=competency.competency_type)

    def delete_ccompetency(self,competency=None):
        if not isinstance(competency, Competency):
            raise TypeError()
        with self.__get_cursor() as cursor:
            cursor.execute('delete from competencies where competency_id=:id',id=competency.competency_id)

    def get_user(self, email):
        if not isinstance(email, str):
            raise TypeError()
        with self.__conn.cursor() as cursor:
            results = cursor.execute('select id, email, password, name from blogapp_users where email=:email', email=email)
            for row in results:
                user = User(id=row[0], email=row[1],
                    password=row[2], name=row[3])
                return user
        return None
    
    def get_user_by_id(self, id):
        if not isinstance(id, int):
            raise TypeError()
        with self.__conn.cursor() as cursor:
            results = cursor.execute('select id, email, password, name from blogapp_users where id=:id', id=id)
            for row in results:
                user = User(id=row[0], email=row[1],
                    password=row[2], name=row[3])
                return user
        return None
