from flask_wtf import FlaskForm
from flask import jsonify
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

class Course:
    def __init__(self,course_number,course_title,theory_hours,lab_hours,
                 homework_hours,description,domain_id,term_id): 
        if not isinstance(course_number,str):
            raise TypeError()
        if not isinstance(course_title,str):
            raise TypeError()
        if not isinstance(theory_hours,int):
            raise TypeError()
        if not isinstance(lab_hours,int):
            raise TypeError()
        if not isinstance(homework_hours,int):
            raise TypeError()
        if not isinstance(description,str):
            raise TypeError()
        if not isinstance(domain_id,str):
            raise TypeError()
        if not isinstance(term_id,str):
            raise TypeError()
        self.course_number=course_number
        self.course_title=course_title
        self.theory_hours=theory_hours
        self.lab_hours=lab_hours
        self.homework_hours=homework_hours
        self.description=description
        self.domain_id=domain_id
        self.term_id=term_id
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
        return Course(json['course_number'],json['course_title'],json['theory_hours'],json['lab_hours'],
                      json['homework_hours'],json['description'],json['domain_id'],json['term_id'])
    def to_json(self):
        return jsonify(self.__dict__)
    
class CourseForm(FlaskForm):
    course_number = StringField('course number',validators=[DataRequired()])
    course_title = StringField('course title',validators=[DataRequired()])
    theory_hours = IntegerField('theory hours',validators=[DataRequired()])
    lab_hours = IntegerField('lab hours',validators=[DataRequired()]),
    homework_hours = IntegerField('homework hours',validators=[DataRequired()])
    description = StringField('description',validators=[DataRequired()])
    domain_id = IntegerField('domain id',validators=[DataRequired()])
    term_id = IntegerField('term id',validators=[DataRequired()])
