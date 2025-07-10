from .baseclass import BaseClass
from app import db
from .place import Place
from .user import User
from sqlalchemy.orm import validates, relationship
import uuid

class Review(BaseClass):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True, default=lambda: str(uuid.uuid4()))
    text = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    place = db.relationship(
        'Place',
        back_populates='reviews'
    )

    @validates('text')
    def validate_text(self, key, value):
        if not value:
            raise ValueError("Text cannot be empty")
        if not isinstance(value, str):
            raise TypeError("Text must be a string")
        return value

    @validates('rating')
    def validate_rating(self, key, value):
        if not isinstance(value, int):
            raise TypeError("Rating must be an integer")
        super().is_between('Rating', value, 1, 6)
        return value

    @validates('place')
    def validate_place(self, key, value):
        if not isinstance(value, Place):
            raise TypeError("Place must be a place instance")
        return value

    @validates('user')
    def validate_user(self, key, value):
        if not isinstance(value, User):
            raise TypeError("User must be a user instance")
        return value

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place_id,
            'user_id': self.user_id
        }
