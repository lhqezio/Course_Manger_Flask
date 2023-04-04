from flask_wtf import FlaskForm
from flask import jsonify
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

class Course:
    def __init__(self,courseNumber,courseTitle,theoryHours,labHours,
                 homeworkHours,description,domainID,termID): 
        if not isinstance(courseNumber,str):
            raise TypeError()
        if not isinstance(courseTitle,str):
            raise TypeError()
        if not isinstance(theoryHours,int):
            raise TypeError()
        if not isinstance(labHours,int):
            raise TypeError()
        if not isinstance(homeworkHours,int):
            raise TypeError()
        if not isinstance(description,str):
            raise TypeError()
        if not isinstance(domainID,str):
            raise TypeError()
        if not isinstance(termID,str):
            raise TypeError()
        self.courseNumber=courseNumber
        self.courseTitle=courseTitle
        self.theoryHours=theoryHours
        self.labHours=labHours
        self.homeworkHours=homeworkHours
        self.description=description
        self.domainID=domainID
        self.termID=termID
    def __str__(self):
        return f'{self.courseNumber} {self.courseTitle}: {self.theoryHours}-{self.labHours}-{self.homeworkHours}'
    def __repr__(self):
        return f'{self.courseNumber} {self.courseTitle}: {self.theoryHours}-{self.labHours}-{self.homeworkHours}'
    def __eq__(self, other):
        if not isinstance(other,Course):
            raise Exception("Not a course object")
        return self.__dict__ == other.__dict__
    def from_json(json):
        if not isinstance(json,dict):
            raise TypeError("Not a course")
        return Course(json['courseNumber'],json['courseTitle'],json['theoryHours'],json['labHours'],
                      json['homeworkHours'],json['description'],json['domainID'],json['termID'])
    def to_json(self):
        return jsonify(self.__dict__)

class CourseForm(FlaskForm):
    courseNumber = StringField('course number',validators=[DataRequired()])
    courseTitle = StringField('course title',validators=[DataRequired()])
    theoryHours = IntegerField('theory hours',validators=[DataRequired()])
    labHours = IntegerField('lab hours',validators=[DataRequired()]),
    homeworkHours = IntegerField('homework hours',validators=[DataRequired()])
    description = StringField('description',validators=[DataRequired()])
    domainID = IntegerField('domain id',validators=[DataRequired()])
    termID = IntegerField('term id',validators=[DataRequired()])
