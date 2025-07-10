from .baseclass import BaseClass
import re
from app import db
from app import bcrypt
from sqlalchemy.orm import validates, relationship


class User(BaseClass):
    __tablename__ = 'users'
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    places = relationship('Place', back_populates='owner', cascade='all, delete-orphan')
    reviews = relationship('Review', back_populates='user', cascade='all, delete-orphan')

    @validates('first_name', 'last_name')
    def validate_name(self, key, value):
        if not isinstance(value, str):
            raise TypeError(f"{key.replace('_', ' ').capitalize()} must be a string")
        if len(value) > 50:
            raise ValueError(f"{key.replace('_', ' ').capitalize()} must be less than or equal to 50 characters")
        if not re.match(r"^[a-zA-Z\- ]+$", value):
            raise ValueError(f"{key.replace('_', ' ').capitalize()} contains invalid characters")
        return value

    @validates('email')
    def validate_email(self, key, value):
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email format")
        return value

    @validates('is_admin')
    def validate_is_admin(self, key, value):
        if not isinstance(value, bool):
            raise TypeError("is_admin must be a boolean")
        return value

    def hash_password(self, password):
        """Hash the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
    
    def add_place(self, place):
        self.places.append(place)
        
    def add_review(self, review):
        """Add a review to the user's list of reviews."""
        self.reviews.append(review)

    def delete_review(self, review):
        """Remove a review from the user's list of reviews."""
        if review in self.reviews:
            self.reviews.remove(review)


    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        }
