from flask_wtf import FlaskForm
from flask import jsonify
from wtforms import StringField, SelectMultipleField, SelectField, TextAreaField, widgets
from wtforms.validators import DataRequired
from CourseManager.element import Element

class Competency:
    def __init__(self,competency_id,competency,competency_achievement,competency_type,elements):
        if not isinstance(competency_id,str):
            raise TypeError("wrong ID")
        if not isinstance(competency,str):
            raise TypeError("bad competency name")
        if not isinstance(competency_achievement,str):
            raise TypeError("bad achievement")
        if not isinstance(competency_type,str):
            raise TypeError("bad type")
        for el in elements:
            if not isinstance(el,Element):
                raise TypeError("no elem", el)
        self.competency_id=competency_id
        self.competency=competency
        self.competency_achievement=competency_achievement
        self.competency_type=competency_type
        self.elements=elements
    def __str__(self):
        return f'{self.competency_id} {self.competency}'
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
    competency_id = StringField('competency id',validators=[DataRequired()])
    competency = StringField('competency',validators=[DataRequired()])
    competency_achievement = TextAreaField('competency achievement',validators=[DataRequired()])
    competency_type = SelectField('competency type',choices=[('Mandatory','Mandatory'),('Optional','Optional')], validators=[DataRequired()])
    elements=SelectMultipleField('elements')

#,widget = widgets.ListWidget(prefix_label=False),option_widget = widgets.CheckboxInput()
#https://stackoverflow.com/questions/70563907/display-wtforms-selectmultiplefield-display-as-drop-down-and-not-list