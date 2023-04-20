from flask import jsonify

class Element:
    def __init__(self,element_id,element_order,element,element_criteria,competency_id): 
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
        self.element_id=element_id
        self.element_order=element_order
        self.element=element
        self.element_criteria=element_criteria
        self.competency_id=competency_id
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
    