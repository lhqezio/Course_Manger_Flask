from flask_wtf import FlaskForm
from flask import jsonify
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

class Competency:
    def __init__(self,competencyID,competency,competencyAchievement,competencyType):
        if not isinstance(competencyID,int):
            raise TypeError()
        if not isinstance(competency,str):
            raise TypeError()
        if not isinstance(competencyAchievement,str):
            raise TypeError()
        if not isinstance(competencyType,str):
            raise TypeError()
        self.competencyID=competencyID
        self.competency=competency
        self.competencyAchievement=competencyAchievement
        self.competencyType=competencyType
    def __str__(self):
        return f'{self.competencyID} {self.competency}: {self.competencyAchievement} type:{self.competencyType}'
    def __repr__(self):
        return f'{self.competencyID} {self.competency}: {self.competencyAchievement} type:{self.competencyType}'
    def __eq__(self, other):
        if not isinstance(other,Competency):
            raise Exception("Not a competency object")
        return self.__dict__ == other.__dict__
    def from_json(json):
        if not isinstance(json,dict):
            raise TypeError("Not a competency")
        return Competency(json['competencyID'],json['competency'],json['competencyAchievement'],json['labHours'])
    def to_json(self):
        return jsonify(self.__dict__)
    
class CompetencyForm(FlaskForm):
    competencyID = IntegerField('competency id',validators=[DataRequired()])
    competency = StringField('competency',validators=[DataRequired()])
    competencyAchievement = StringField('competency achievement',validators=[DataRequired()])
    competencyType = StringField('competency type',validators=[DataRequired()])
