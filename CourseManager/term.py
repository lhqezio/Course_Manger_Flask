
from flask import jsonify

class Term:
    def __init__(self,term_id,term_name): 
        if not isinstance(term_name,str):
            raise TypeError()
        if not isinstance(term_id,int):
            raise TypeError()
        self.term_id=term_id
        self.term_name=term_name
    def __str__(self):
        return f'Term: {self.term_id} {self.term_name}'
    def __repr__(self):
        return f'Term: {self.term_id} {self.term_name}'
    def __eq__(self, other):
        if not isinstance(other,Term):
            raise Exception("Not a course object")
        return self.__dict__ == other.__dict__
    def from_json(json):
        if not isinstance(json,dict):
            raise TypeError("Not a Term")
        return Term(json['term_id'],json['term_name'])
    def to_json(self):
        return jsonify(self.__dict__)
    
