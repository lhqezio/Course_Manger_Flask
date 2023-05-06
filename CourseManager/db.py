import os
import oracledb
from CourseManager.course import Course
from CourseManager.competency import Competency
from CourseManager.user import User
from CourseManager.term import Term
from CourseManager.domain import Domain
from CourseManager.element import Element
from CourseManager.user import User
from werkzeug.security import check_password_hash, generate_password_hash

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

    def commit(self):
        if self.__conn:
            self.__conn.commit()
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

    def get_domain(self, dom_id):
            with self.__get_cursor() as cursor:
                results = cursor.execute('select domain_id, domain, domain_description from domains where domain_id=:id', id=dom_id)
                for row in results:
                    return Domain(domain_id=row[0], domain=row[1], domain_description=row[2])

    def get_domains(self):
        domains = []
        with self.__get_cursor() as cursor:
            results = cursor.execute('select domain_id, domain, domain_description from domains')
            for row in results:
                domain = Domain(domain_id=row[0], domain=row[1], domain_description=row[2])
                domains.append(domain)
        return domains

    def get_term(self, term_id):
            with self.__get_cursor() as cursor:
                results = cursor.execute('select term_id,term_name from terms where term_id=:id', id=term_id)
                for row in results:
                    return Term(term_id=row[0], term_name=row[1])

    def get_terms(self):
        terms = []
        with self.__get_cursor() as cursor:
            results = cursor.execute('select term_id, term_name from terms ORDER BY(term_id)')
            for row in results:
                term = Term(term_id=row[0], term_name=row[1])
                terms.append(term)
        return terms
    
    def get_term_for_course(self,course_id):
        with self.__get_cursor() as cursor:
            results = cursor.execute('select term_id, term_name from view_courses_terms where course_id=:id',id=course_id)
            for row in results:
                term = Term(term_id=row[0], term_name=row[1])
                return term
            return None
            
    def get_domain_for_course(self,course_id):
        with self.__get_cursor() as cursor:
            results = cursor.execute('select domain_id,domain,domain_description from view_courses_domains where course_id=:id',id=course_id)
            for row in results:
                domain = Domain(domain_id=row[0],domain=row[1],
                    domain_description=row[2])
                return domain
            return None
            
    def get_elems_from_course(self,course_id):
        if not isinstance(course_id, str):
            raise TypeError()
        course_elems = []
        with self.__get_cursor() as cursor:
            results = cursor.execute('select v.element_id, v.element_order, v.element, v.element_criteria, v.competency_id, e.element_hours from view_courses_elements_competencies v inner join courses_elements e using(course_id) where course_id:id',id=course_id)
            for row in results:
                element = Element(element_id=row[0],element_order=row[1],element=row[2],element_criteria=row[3],competency_id=row[4], hours=row[5])
                course_elems.append(element)
        return course_elems
    
    def get_course(self,course_id):
        if not isinstance(course_id, str):
            raise TypeError()
        with self.__get_cursor() as cursor:
            results = cursor.execute('select course_id,course_title,theory_hours,lab_hours,work_hours,description,term_id,term_name,domain_id,domain,domain_description from view_courses_terms inner join domains using(domain_id) WHERE COURSE_ID = :course_id',course_id=course_id)
            for row in results:
                term=Term(term_id=row[6],term_name=row[7])
                domain=Domain(domain_id=row[8],domain=row[9],domain_description=row[10])
                course_competencies=self.get_competencies_from_courses(course_id=row[0])
                course = Course(course_number=row[0],course_title=row[1],theory_hours=row[2],lab_hours=row[3],homework_hours=row[4],description=row[5],domain=domain,term=term,competencies=course_competencies)
                return course
        return None
    
    def get_courses(self):
        courses=[]
        with self.__get_cursor() as cursor:
            results = cursor.execute('select course_id,course_title,theory_hours,lab_hours,work_hours,description,term_id,term_name,domain_id,domain,domain_description from view_courses_terms inner join domains using(domain_id)')
            for row in results:
                term=Term(term_id=row[6],term_name=row[7])
                domain=Domain(domain_id=row[8],domain=row[9],domain_description=row[10])
                course_competencies=self.get_competencies_from_courses(row[0])
                course = Course(course_number=row[0],course_title=row[1],theory_hours=row[2],lab_hours=row[3],homework_hours=row[4],description=row[5],domain=domain,term=term,competencies=course_competencies)
                courses.append(course)
        return courses
    
    def get_courses_from_domain(self,domain_id):
        if not isinstance(domain_id, str):
            raise TypeError()
        courses = []
        with self.__get_cursor() as cursor:
            results = cursor.execute('select course_id,course_title,theory_hours,lab_hours,work_hours,description,term_id,term_name,domain_id,domain,domain_description from view_courses_terms inner join domains using(domain_id) where domain_id=:id',id=domain_id)
            for row in results:
                term=Term(term_id=row[6],term_name=row[7])
                domain=Domain(domain_id=row[8],domain=row[9],domain_description=row[10])
                course_competencies=self.get_competencies_from_courses(row[0])
                course = Course(course_number=row[0],course_title=row[1],theory_hours=row[2],lab_hours=row[3],homework_hours=row[4],description=row[5],domain=domain,term=term,competencies=course_competencies)
                courses.append(course)
        return courses
    
    def get_courses_from_term(self,term_id):
        if not isinstance(term_id, str):
            raise TypeError()
        courses = []
        with self.__get_cursor() as cursor:
            results = cursor.execute('select course_id,course_title,theory_hours,lab_hours,work_hours,description,term_id,term_name,domain_id,domain,domain_description from view_courses_terms inner join domains using(domain_id) WHERE TERM_ID = :term_id',term_id = term_id)
            for row in results:
                term=Term(term_id=row[6],term_name=row[7])
                domain=Domain(domain_id=row[8],domain=row[9],domain_description=row[10])
                course_competencies=self.get_competencies_from_courses(row[0])
                course = Course(course_number=row[0],course_title=row[1],theory_hours=row[2],lab_hours=row[3],homework_hours=row[4],description=row[5],domain=domain,term=term,competencies=course_competencies)
                courses.append(course)
        return courses
    
    def get_elems_from_competency(self,comp_id):
        if not isinstance(comp_id, str):
            raise TypeError()
        competency_elems = [] 
        with self.__get_cursor() as cursor:
            results = cursor.execute('select element_id, element_order, element, element_criteria, competency_id from elements where competency_id=:id',id=comp_id)
            for row in results:
                element = Element(element_id=row[0],element_order=row[1],element=row[2],element_criteria=row[3],competency_id=row[4],hours=0)
                competency_elems.append(element)
        return competency_elems
    
    def get_elems_of_competency(self,competency_id):
        if not isinstance(competency_id, int):
            raise TypeError()
        competency_elems = [] 
        with self.__get_cursor() as cursor:
            results = cursor.execute('select element_id, element_order, element, element_criteria, competency_id from elements where competency_id=:id',id=competency_id)
            for row in results:
                element = Element(element_id=row[0],element_order=row[1],element=row[2],element_criteria=row[3],competency_id=row[4],hours=0)
                competency_elems.append(element)
        return competency_elems
    
    def get_competency(self,competency_id):
        if not isinstance(competency_id, str):
            raise TypeError()
        with self.__get_cursor() as cursor:
            results = cursor.execute('select competency_id,competency,competency_achievement,competency_type from competencies where competency_id = :id',id=competency_id)
            for row in results:
                elements=self.get_elems_from_competency(competency_id)
                competency = Competency(competency_id=row[0],competency=row[1],competency_achievement=row[2],competency_type=row[3],elements=elements)
                return competency
        return None
    
    def get_competencies(self):
        competencies = [] 
        with self.__get_cursor() as cursor:
            results = cursor.execute('select competency_id,competency,competency_achievement,competency_type from competencies')
            for row in results:
                elements=self.get_elems_from_competency(comp_id=row[0])
                competency = Competency(competency_id=row[0],competency=row[1],competency_achievement=row[2],competency_type=row[3],elements=elements)
                competencies.append(competency)
        return competencies

    def get_competencies_from_courses(self,course_id):
        if not isinstance(course_id, str):
            raise TypeError()
        course_competencies = [] 
        with self.__get_cursor() as cursor:
            results = cursor.execute('select distinct competency_id,competency,competency_achievement,competency_type from view_courses_elements_competencies where course_id=:id',id=course_id)  
            for row in results:
                elements=self.course_elems_by_competency(course_id,row[0])
                competency = Competency(competency_id=row[0],competency=row[1],competency_achievement=row[2],competency_type=row[3],elements=elements)
                course_competencies.append(competency)
        return course_competencies
    
    def course_elems_by_competency(self,course_id,comp_id):
        if not isinstance(course_id, str):
            raise TypeError()
        if not isinstance(comp_id, str):
            raise TypeError()
        elements=[]
        with self.__get_cursor() as cursor:
            elems = cursor.execute('select element_id,element_order,element,element_criteria,competency_id, element_hours from view_courses_elements_competencies where course_id=:id and competency_id=:cid',id=course_id,cid=comp_id)
            for e in elems:
                element=Element(element_id=e[0],element_order=e[1],element=e[2],element_criteria=e[3],competency_id=e[4], hours=e[5])
                elements.append(element)
        return elements
    
    def course_elem_in_competency(self,course_id,comp_id):
        if not isinstance(course_id, str):
            raise TypeError()
        if not isinstance(comp_id, str):
            raise TypeError()
        with self.__get_cursor() as cursor:
            elems = cursor.execute('select element_id,element_order,element,element_criteria,competency_id, element_hours from view_courses_elements_competencies where course_id=:id and competency_id=:cid',id=course_id,cid=comp_id)
            for e in elems:
                element=Element(element_id=e[0],element_order=e[1],element=e[2],element_criteria=e[3],competency_id=e[4], hours=e[5])
            return element
    
    def get_competency_elemhrs_from_course(self,course_id):
        if not isinstance(course_id, str):
            raise TypeError("wrong course id")
        course_elems = [] #elems that are already part of the course
        with self.__get_cursor() as cursor:
            results = cursor.execute('select element_id,element_order,element,element_criteria,competency_id, element_hours from view_courses_elements_competencies where course_id=:id',id=course_id)  
            for row in results:
                element = Element(element_id=row[0],element_order=row[1],element=row[2],element_criteria=row[3],competency_id=row[4], hours=row[5])
                course_elems.append(element)
        return course_elems
    
    def get_element(self, elem_id):
        with self.__get_cursor() as cursor:
            results = cursor.execute('select e.element_id,e.element_order, e.element, e.element_criteria, e.competency_id, h.element_hours from elements e left outer join courses_elements h on e.element_id=h.element_id where e.element_id=:id', id=elem_id)
            for row in results:
                return Element(element_id=row[0],element_order=row[1],element=row[2],element_criteria=row[3],competency_id=row[4], hours=row[5])

    def get_elems(self):
        elements = [] 
        with self.__get_cursor() as cursor:
            results = cursor.execute('select element_id, element_order,  element, element_criteria, competency_id from elements')
            for row in results:
                element = Element(element_id=row[0],element_order=row[1],element=row[2],element_criteria=row[3],competency_id=row[4], hours=0)
                elements.append(element)
        return elements
    
    def get_elems_from_course(self,course_id):
        if not isinstance(course_id, str):
            raise TypeError()
        course_elems = []
        with self.__get_cursor() as cursor:
            results = cursor.execute('select e.element_id, e.element_order, e.element, e.element_criteria, e.competency_id, h.element_hours from view_courses_elements_competencies e left outer join courses_elements h on e.element_id=h.element_id where e.course_id=:id and h.element_hours!=0',id=course_id)
            for row in results:
                element = Element(element_id=row[0],element_order=row[1],element=row[2],element_criteria=row[3],competency_id=row[4], hours=row[5])
                course_elems.append(element)
        return course_elems

    def add_course(self,course=None):
        if not isinstance(course, Course):
            raise TypeError()
        with self.__get_cursor() as cursor:
            domain_id=course.domain.domain_id
            term_id=course.term.term_id
            cursor.execute('insert into courses values(:id,:title,:thrs,:lhrs,:hhrs,:descr,:dom_id,:term_id)',
                            id=course.course_number,title=course.course_title,thrs=course.theory_hours,lhrs=course.lab_hours,
                            hhrs=course.homework_hours,descr=course.description,dom_id=domain_id,term_id=term_id)
        #add competencies
        for comp in course.competencies:
            with self.__get_cursor() as cursor:
                elements=self.get_elems_from_competency(comp_id=comp.competency_id)
                for el in elements:
                    cursor.execute('insert into courses_elements values(:cid,:eid,0)',cid=course.course_number,eid=el.element_id)
    
    def update_course(self,course=None):
        if not isinstance(course, Course):
            raise TypeError()
        with self.__get_cursor() as cursor:
            domain_id=course.domain.domain_id
            term_id=course.term.term_id
            #update course info
            cursor.execute('update courses set course_title=:title,theory_hours=:thrs,lab_hours=:lhrs,work_hours=:whrs,description=:descr,domain_id=:dom_id,term_id=:t_id WHERE course_id=:id',
                            id=course.course_number,title=course.course_title,thrs=course.theory_hours,lhrs=course.lab_hours,
                            whrs=course.homework_hours,descr=course.description,dom_id=domain_id,t_id=term_id)
            current_competencies=self.get_competencies_from_courses(course_id=course.course_number)
        #new competencies
        for comp in course.competencies:
            if comp not in current_competencies:
                with self.__get_cursor() as cursor:
                    elements=self.get_elems_from_competency(comp_id=comp.competency_id)
                    for el in elements:
                        cursor.execute('insert into courses_elements values(:cid,:eid,0)',cid=course.course_number,eid=el.element_id)
        #remove competencies
        for comp in current_competencies:
            if comp not in course.competencies:
                elements=self.get_elems_of_competency(comp.competency_id)
                for el in elements:
                    with self.__get_cursor() as cursor:
                        cursor.execute('delete from courses_elements where course_id=:cid and element_id=:eid',cid=course.course_number,eids=el.element_id)
         
    def update_course_elem_hrs(self,course_id,element_id,hours):
        if not isinstance(course_id, str):
            raise TypeError()
        if not isinstance(int(element_id), int):
            raise TypeError()
        #set course teaching elem hours
        with self.__get_cursor() as cursor:
                cursor.execute('delete from courses_elements where course_id=:course_id and element_id=:el_id',course_id=course_id,el_id=element_id)
        if hours>0:
            with self.__get_cursor() as cursor:
                    cursor.execute('insert into courses_elements values(:course_id,:el_id,:hours)',course_id=course_id,el_id=element_id, hours=hours) 

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
            with self.__get_cursor() as cursor:
                for ele in competency.elements:
                    cursor.execute('update elements set competency_id=:comp_id WHERE element_id=:elem_id',
                            comp_id=competency.competency_id, elem_id=ele.element_id)

    def update_competency(self,competency=None):
        if not isinstance(competency, Competency):
            raise TypeError()
        with self.__get_cursor() as cursor:
            cursor.execute('update competencies set competency=:name,competency_achievement=:achievement,competency_type=:type WHERE competency_id=:id',
                            id=competency.competency_id,name=competency.competency,
                            achievement=competency.competency_achievement,type=competency.competency_type)
        with self.__get_cursor() as cursor:
            for ele in competency.elements:
                cursor.execute('update elements set competency_id=:comp_id WHERE element_id=:elem_id',
                            comp_id=competency.competency_id, elem_id=ele.element_id)
            

    def delete_competency(self,competency=None):
        if not isinstance(competency, Competency):
            raise TypeError()
        with self.__get_cursor() as cursor:
            cursor.execute('delete from competencies where competency_id=:id',id=competency.competency_id)

    def get_user(self, email):
        if not isinstance(email, str):
            raise TypeError()
        with self.__conn.cursor() as cursor:
            results = cursor.execute('select id, email, password, name, avatar, role from coursemanager_users where email=:email', email=email)
            for row in results:
                user = User(email=row[1],
                    password=row[2], name=row[3],avatar_path=row[4],role=row[5])
                return user
        return None

    def get_users(self):
        users = []
        with self.__conn.cursor() as cursor:
            results = cursor.execute('select id, email, password, name,avatar,role from coursemanager_users')
            for row in results:
                user = User(email=row[1],
                    password=row[2], name=row[3], avatar_path=row[4], role=row[5])
                users.append(user)
        return users
    
    def update_user(self,user,old_email):
        if not isinstance(user, User):
            raise TypeError()
        with self.__conn.cursor() as cursor:
            cursor.execute('update coursemanager_users set email=:email, password=:password, role=:role, name=:name, avatar=:avatar where email=:old_email',
                email=user.email, password=user.password, name=user.name,role=user.role,old_email=old_email,avatar=user.avatar_path)
    def add_user(self,user):
        if not isinstance(user, User):
            raise TypeError()
        with self.__conn.cursor() as cursor:
            cursor.execute('insert into coursemanager_users (email,password,role,name,avatar) values(:email,:password,:role,:name,:avatar)',
                email=user.email, password=user.password, name=user.name,role=user.role,avatar=user.avatar_path)
    
    def remove_user(self,email):
        if not isinstance(email, str):
            raise TypeError()
        with self.__conn.cursor() as cursor:
            cursor.execute('delete from coursemanager_users where email=:email',
                email=email)
    