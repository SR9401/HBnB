from .basemodel import BaseModel
import re
from app import db
class User(BaseModel):
    __tablename__ = 'users'
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)


    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email format")

        if self._email == value:
            return
        
        if value in User.emails:
            raise ValueError("Email already exists")

        # Supprimer l'ancien email du set si existant
        if self._email:
            User.emails.discard(self._email)

        self._email = value
        User.emails.add(value)

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        from app import bcrypt
        if not isinstance(value, str):
            raise TypeError("Password must be a string")
        hashed = bcrypt.generate_password_hash(value).decode('utf-8')
        self.__password = hashed

    def verify_password(self, password):
        from app import bcrypt
        if not self.__password:
            return False
        return bcrypt.check_password_hash(self.__password, password)


    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        }
