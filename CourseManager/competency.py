from flask_wtf import FlaskForm
from flask import jsonify
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

class Competency:
    def __init__(self,competency_id,competency,competency_achievement,competency_type):
        if not isinstance(competency_id,str):
            raise TypeError()
        if not isinstance(competency,str):
            raise TypeError()
        if not isinstance(competency_achievement,str):
            raise TypeError()
        if not isinstance(competency_type,str):
            raise TypeError()
        self.competency_id=competency_id
        self.competency=competency
        self.competency_achievement=competency_achievement
        self.competency_type=competency_type
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
        return Competency(json['competency_id'],json['competency'],json['competency_achievement'],json['competency_type'])
    def to_json(self):
        return jsonify(self.__dict__)
    
class CompetencyForm(FlaskForm):
    competency_id = IntegerField('competency id',validators=[DataRequired()])
    competency = StringField('competency',validators=[DataRequired()])
    competency_achievement = StringField('competency achievement',validators=[DataRequired()])
    competency_type = StringField('competency type',validators=[DataRequired()])
