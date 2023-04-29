from flask_wtf import FlaskForm
from flask import jsonify
from wtforms import StringField, IntegerField, SelectField, SelectMultipleField, TextAreaField, widgets
from wtforms.validators import DataRequired, NumberRange
from CourseManager.domain import Domain
from CourseManager.term import Term
from CourseManager.competency import Competency

class Course:
    def __init__(self,course_number,course_title,theory_hours,lab_hours,
                 homework_hours,description,domain,term,competencies): 
        if not isinstance(course_number,str):
            raise TypeError("bad course id")
        if not isinstance(course_title,str):
            raise TypeError("bad course title")
        if not isinstance(theory_hours,int) or theory_hours<0:
            raise TypeError("bad theory hours")
        if not isinstance(lab_hours,int) or lab_hours<0:
            raise TypeError("bad lab hours")
        if not isinstance(homework_hours,int) or homework_hours<0:
            raise TypeError("bad homework hours")
        if not isinstance(description,str):
            raise TypeError("bad description")
        if not isinstance(domain,Domain):
            raise TypeError("bad domain")
        if not isinstance(term,Term):
            raise TypeError("bad term")
        for comp in competencies:
            if not isinstance(comp,Competency):
                raise TypeError("not competency")
        self.course_number=course_number
        self.course_title=course_title
        self.theory_hours=theory_hours
        self.lab_hours=lab_hours
        self.homework_hours=homework_hours
        self.description=description
        self.domain=domain
        self.term=term
        self.competencies=competencies
    def __str__(self):
        return f'{self.course_number} {self.course_title}: {self.theory_hours}-{self.lab_hours}-{self.homework_hours}'
    def __repr__(self):
        return f'{self.course_number} {self.course_title}: {self.theory_hours}-{self.lab_hours}-{self.homework_hours}'
    def __eq__(self, other):
        if not isinstance(other,Course):
            raise Exception("Not a course object")
        return self.__dict__ == other.__dict__
    def from_json(json):
        if not isinstance(json,dict):
            raise TypeError("Not a course")
        term=Term.from_json(json['term'])
        domain=Domain.from_json(json['domain'])
        competencies=[]
        for comp in json['competencies']:
            comp=Competency.from_json(comp)
            competencies.append(comp)
        return Course(json['course_number'],json['course_title'],json['theory_hours'],json['lab_hours'],
                      json['homework_hours'],json['description'],domain,term,competencies)
    def to_json(self):
        return jsonify(self.__dict__)
    
class CourseForm(FlaskForm):
    course_number = StringField('course number',validators=[DataRequired()])
    course_title = StringField('course title',validators=[DataRequired()])
    theory_hours = IntegerField('theory hours',validators=[NumberRange(min=0, message='Invalid length'),DataRequired()])
    lab_hours = IntegerField('lab hours',validators=[NumberRange(min=0, message='Invalid length'),DataRequired()])
    homework_hours = IntegerField('homework hours',validators=[NumberRange(min=0, message='Invalid length'),DataRequired()])
    description = TextAreaField('description',validators=[DataRequired()])
    domain_id = SelectField('domain',validators=[DataRequired()])
    term_id = SelectField('term',validators=[DataRequired()])
    competencies = SelectMultipleField('competencies')
    #,widget = widgets.ListWidget(prefix_label=False),option_widget = widgets.CheckboxInput()
    
