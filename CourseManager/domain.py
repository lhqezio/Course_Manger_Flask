from flask import jsonify

class Domain:
    def __init__(self,domain_id,domain,domain_description): 
        if not isinstance(domain,str):
            raise TypeError()
        if not isinstance(domain_id,int):
            raise TypeError()
        if not isinstance(domain_description,str):
            raise TypeError()
        self.domain_id=domain_id
        self.domain=domain
        self.domain_description=domain_description
    def __str__(self):
        return f'Domain: {self.domain_id} {self.domain}'
    def __repr__(self):
        return f'Domain: {self.domain_id} {self.domain}'
    def __eq__(self, other):
        if not isinstance(other,Domain):
            raise Exception("Not a domain object")
        return self.__dict__ == other.__dict__
    def from_json(json):
        if not isinstance(json,dict):
            raise TypeError("Not a domain")
        return Domain(json['domain_id'],json['domain'],json['domain_description'])
    def to_json(self):
        return jsonify(self.__dict__)