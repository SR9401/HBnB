from .baseclass import BaseClass
from app import db
from sqlalchemy.orm import validates

class Amenity(BaseClass):
    __tablename__ = 'amenities'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)

    @validates('name')
    def validate_name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if not value:
            raise ValueError("Name cannot be empty")
        if len(value) > 50:
            raise ValueError("Name must be 50 characters max")
        return value

    def update(self, data):
        return super().update(data)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
