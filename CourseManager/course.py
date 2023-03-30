#from flask_wtf import FlaskForm
# from flask import jsonify
# from wtforms import StringField
# from wtforms.validators import DataRequired

class Course:
    def __init__(self,courseNumber,courseTitle,theoryHours,labHours,
                 homeworkHours,description,domainID,term): 
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
        if not isinstance(term,str):
            raise TypeError()
        self.courseNumber=courseNumber
        self.courseTitle=courseTitle
        self.theoryHours=theoryHours
        self.labHours=labHours
        self.homeworkHours=homeworkHours
        self.description=description
        self.domainID=domainID
        self.term=term
    def __str__(self):
        return f''
    def __eq__(self, obj):
        if not isinstance(obj,Course):
            raise Exception("Not a course object")
        if(self.name!=obj.name):
            return False
        return True
    def from_json(json):
        if not isinstance(json,dict):
            raise TypeError("Not an Address")
        #return Cpourse(json['name'],json['street'],json['city'],json['province'])
    def to_json(self):
        #return jsonify(self.__dict__)