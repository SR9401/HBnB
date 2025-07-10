from .baseclass import BaseClass
from app import db
from sqlalchemy.orm import validates, relationship
from .place_amenity import place_amenity
import uuid

class Amenity(BaseClass):
    __tablename__ = 'amenities'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), nullable=False)
    
    places = relationship(
        "Place",
        secondary=place_amenity,
        back_populates="amenities"
    )

    @validates('name')
    def validate_name(self, key, value):
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