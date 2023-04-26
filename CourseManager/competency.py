from flask_wtf import FlaskForm
from flask import jsonify
from wtforms import StringField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired
from CourseManager.element import Element

class Competency:
    def __init__(self,competency_id,competency,competency_achievement,competency_type,elements):
        if not isinstance(competency_id,str):
            raise TypeError()
        if not isinstance(competency,str):
            raise TypeError()
        if not isinstance(competency_achievement,str):
            raise TypeError()
        if not isinstance(competency_type,str):
            raise TypeError()
        for el in elements:
            if not isinstance(el,Element):
                raise TypeError()
        self.competency_id=competency_id
        self.competency=competency
        self.competency_achievement=competency_achievement
        self.competency_type=competency_type
        self.elements=elements
    def __str__(self):
        return f'{self.competency_id} {self.competency}: {self.competency_achievement} type:{self.competency_type}'
    def __repr__(self):
        return f'{self.competency_id} {self.competency}: {self.competency_achievement} type:{self.competency_type}'
    def __eq__(self, other):
        if not isinstance(other,Competency):
            raise Exception("Not a competency object")
        return self.__dict__ == other.__dict__
    def from_json(json):
        if not isinstance(json,dict):
            raise TypeError("Not a competency")
        elements=[]
        for el in json['elements']:
            element=Element.from_json(el)
            elements.append(element)
        return Competency(json['competency_id'],json['competency'],json['competency_achievement'],json['competency_type'],elements)
    def to_json(self):
        return jsonify(self.__dict__)
    
class CompetencyForm(FlaskForm):
    competency_id = IntegerField('competency id',validators=[DataRequired()])
    competency = StringField('competency',validators=[DataRequired()])
    competency_achievement = StringField('competency achievement',validators=[DataRequired()])
    competency_type = StringField('competency type',validators=[DataRequired()])
    elements=SelectMultipleField('elements',validators=[DataRequired()])

