from app.models.base_model import BaseModel
from app.models.user import User


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self._owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities
    
    
    @property
    def title(self):
        return self.__title
    
    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        if len(value) > 100:
            raise ValueError("Title must be < 100 characters")
        self.__title = value
        self.save()

    @property
    def description(self):
        return self.__description
    
    @description.setter
    def description(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("Description must be a string")
        self.__description = value
        self.save()

    @property
    def price(self):
        return self.__price
    
    @price.setter
    def price(self, value):
        if not isinstance (value, (int, float)):
            raise TypeError("Price must be a float")
        if value < 0:
            raise ValueError("Price must be positive")
        self.__price = value
        self.save()


    @property
    def latitude(self):
        return self.__latitude
    
    @latitude.setter
    def latitude(self, value):
        if not isinstance (value, (int, float)):
            raise TypeError("Latitude must be a float")
        if value < -90.0 or value > 90.0:
            raise ValueError("Latitude must be between -90.0 and 90.0")
        self.__latitude = value
        self.save()

    @property
    def longitude(self):
        return self.__longitude
    
    @longitude.setter
    def longitude(self, value):
        if not isinstance (value, float):
            raise TypeError("Longitude must be a float")
        if value < -180.0 or value > 180.0:
            raise ValueError("Longitude must be between -180.0 and 180.0")
        self.__longitude = value
        self.save()        


    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, value):
         if not isinstance(value, User):
            raise TypeError("Owner must be a User instance")
         self.__owner = value
         self.save()

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def to_dict(self, full=False):
        base = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner.id if hasattr(self.owner, 'id') else self.owner,
        }