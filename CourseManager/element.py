from flask import jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired

class Element:
    def __init__(self,element_id,element_order,element,element_criteria,competency_id, hours): 
        if not isinstance(element,str):
            raise TypeError()
        if not isinstance(element_id,int):
            raise TypeError()
        if not isinstance(element_order,int):
            raise TypeError()
        if not isinstance(element_criteria,str):
            raise TypeError()
        if not isinstance(competency_id,str):
            raise TypeError()
        if not isinstance(competency_id,str):
            raise TypeError()
        if not isinstance(hours,int):
            hours=0
        self.element_id=element_id
        self.element_order=element_order
        self.element=element
        self.element_criteria=element_criteria
        self.competency_id=competency_id
        self.hours=hours
    def __str__(self):
        return f'Element: {self.element_id} {self.element}'
    def __repr__(self):
         return f'Element: {self.element_id} {self.element}'
    def __eq__(self, other):
        if not isinstance(other,Element):
            raise Exception("Not an element object")
        return self.__dict__ == other.__dict__
    def from_json(json):
        if not isinstance(json,dict):
            raise TypeError("Not an Element")
        return Element(json['element_id'],json['element_order'],json['element'],json['element_criteria'],json['competency_id'])
    def to_json(self):
        return jsonify(self.__dict__)
    
class ElementForm(FlaskForm):
    element_id = IntegerField('element id',validators=[DataRequired()])
    element_order = IntegerField('element order',validators=[DataRequired()])
    element = StringField('element',validators=[DataRequired()])
    element_criteria = StringField('element criteria',validators=[DataRequired()])
    competency_id= SelectField('competency id',validators=[DataRequired()])
    hours = IntegerField('element hours',validators=[DataRequired()])

    