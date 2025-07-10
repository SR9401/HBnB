from .baseclass import BaseClass
from app import db
from sqlalchemy.orm import validates, relationship
from sqlalchemy import Table, Column, Integer, ForeignKey
import uuid
from .user import User
from .place_amenity import place_amenity

class Place(BaseClass):
    __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(36))
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    owner = relationship('User', back_populates='places')
    
    amenities = relationship(
        "Amenity",
        secondary=place_amenity,
        back_populates="places"
    )

    reviews = relationship('Review', back_populates='place', cascade='all, delete-orphan')
    
    @validates('title')
    def validate_title(self, key, value):
        if not value:
            raise ValueError("Title cannot be empty")
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        if len(value) > 50:
            raise ValueError("Title must be 50 characters max")
        return value

    @validates('price')
    def validate_price(self, key, value):
        if not isinstance(value, float) and not isinstance(value, int):
            raise TypeError("Price must be a float")
        if value < 0:
            raise ValueError("Price must be positive.")
        return float(value)

    @validates('latitude')
    def validate_latitude(self, key, value):
        if not isinstance(value, float):
            raise TypeError("Latitude must be a float")
        if not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        return float(value)
    
    @validates('longitude')
    def validate_longitude(self, key, value):
        if not isinstance(value, float):
            raise TypeError("Longitude must be a float")
        if not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 et 180.")
        return float(value)

    @validates('owner_id')
    def validate_owner_id(self, key, value):
        if not isinstance(value, User):
            raise TypeError("Owner must be a user instance")
        return value

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)
    
    def delete_review(self, review):
        """Add an amenity to the place."""
        self.reviews.remove(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id
        }
    
    def to_dict_list(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner': self.owner.to_dict() if self.owner else None,
            'amenities': [a.to_dict() for a in self.amenities],
            'reviews': [r.to_dict() for r in self.reviews]
        }
