#from flask_wtf import FlaskForm
# from flask import jsonify
# from wtforms import StringField
# from wtforms.validators import DataRequired

class Course:
    def __init__(self,courseNumber,courseTitle,theoryHours,labHours,
                 homeworkHours,description,domainID,term): 
        if not isinstance(name,str):
            raise Exception("Firstname should be a string")
        if not isinstance(street,str):
            raise Exception("street should be a string")
        if not isinstance(city,str):
            raise Exception("city should be a string")
        if not isinstance(province,str):
            raise Exception("province should be a string")
        self.courseNumber=courseNumber
        self.courseTitle=courseTitle
        self.theoryHours=theoryHours
        self.labHours=labHours
        self.homeworkHours=homeworkHours
        self.description=description
        self.domainID=domainID
        self.term=term
    def __str__(self):
        return f'Name:{self.name}:  street:{self.street},  city:{self.city},  province:{self.province}'
    def __eq__(self, obj):
        if not isinstance(obj,Course):
            raise Exception("Not a course object")
        if(self.name!=obj.name):
            return False
        return True
    def from_json(json):
        if not isinstance(json,dict):
            raise TypeError("Not an Address")
        #return Address(json['name'],json['street'],json['city'],json['province'])
    def to_json(self):
        #return jsonify(self.__dict__)