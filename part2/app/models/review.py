from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place

class Review(BaseModel):

    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.user = user
        self.place = place

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise TypeError("Text must be a string")
        if value is None:
            raise ValueError("Text Required")
        self.__text = value
        self.save()

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int):
            raise TypeError("Rating must be integer")
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5")
        self.__rating = value
        self.save()

    @property
    def place(self):
        return self.__place

    @place.setter
    def place(self, value):
        if not isinstance(value, Place):
            raise ValueError("place must be a Place instance")
        self.__place = value
        self.save()

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, value):
        if not isinstance(value, User):
            raise TypeError("user must be a User instance")
        self.__user = value
        self.save()
