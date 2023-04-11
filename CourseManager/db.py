import os
import oracledb

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

    def get_domains(self):
        domains = []
        with self.__conn.cursor() as cursor:
            results = cursor.execute('select domain_id, domain, description from domains')
            for row in results:
                domain = Domain(domain=row[1],
                    description=row[2])
                domain.id = row[0]
                domains.append(domain)
        return domains

    def get_terms(self):
        terms = []
        with self.__conn.cursor() as cursor:
            results = cursor.execute('select term_id, term_name from terms')
            for row in results:
                term = Term(id=row[0],domain=row[1],
                    description=row[2])
                terms.append(term)
        return terms
    
    def get_course(self,course_id):
        with self.__conn.cursor() as cursor:
            results = cursor.execute('SELECT COURSE_ID, COURSE_TITLE, THEORY_HOURS, LAB_HOURS, WORK_HOURS, DESCRIPTION, DOMAIN_ID,TERM_ID FROM COURSES WHERE COURSE_ID LIKE :course_id',course_id=course_id)
            if results.rowcount is not 1:
                raise oracledb.Error
            for row in results:
                course = Course()
        return course
    def get_courses_from_domain(self,domain_id):
        courses = []
        with self.__conn.cursor() as cursor:
            results = cursor.execute('SELECT COURSE_ID, COURSE_TITLE, THEORY_HOURS, LAB_HOURS, WORK_HOURS, DESCRIPTION, DOMAIN_ID,TERM_ID FROM COURSES')
            for row in results:
                course = Course()
                courses.append(course)
        return courses
    def get_courses_from_term(self,term_id):
        courses = []
        with self.__conn.cursor() as cursor:
            results = cursor.execute('SELECT COURSE_ID, COURSE_TITLE, THEORY_HOURS, LAB_HOURS, WORK_HOURS, DESCRIPTION, DOMAIN_ID,TERM_ID FROM COURSES WHERE TERM_ID LIKE :term_id',term_id = term_id)
            for row in results:
                course = Course()
                courses.append(course)
        return courses
    
    def get_courses_from_domain(self,domain_id):
        courses = []
        with self.__conn.cursor() as cursor:
            results = cursor.execute('SELECT COURSE_ID, COURSE_TITLE, THEORY_HOURS, LAB_HOURS, WORK_HOURS, DESCRIPTION, DOMAIN_ID,TERM_ID FROM COURSES WHERE DOMAIN_ID LIKE :domain_id',domain_id = domain_id)
            for row in results:
                course = Course()
                courses.append(course)
        return courses
        

    def get_competencies(self,course_id):
        pass 

    def get_competenciesa_from_courses(self,course_id):
        pass 

    def get_elems(self,comp_id):
        pass

    def get_elems_from_competencies(self,comp_id):
        pass

    def get_elems_from_courses(self,comp_id):
        pass

    def edit_course(self,course=None):
        pass

    def edit_comp(self,competency=None):
        pass

    def edit_elem(self,element=None):
        pass

