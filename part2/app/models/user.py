from app.models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.__is_admin = is_admin

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError("First name must be a string")
        if len(value) > 50:
            raise ValueError("First name must not exceed 50 characters")
        self.__first_name = value

        @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str):
            raise TypeError("Last name must be a string")
        if len(value) > 50:
            raise ValueError("Last name must not exceed 50 characters")
        self.__last_name = value

    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email (self,value)
        if not isinstance(value,str)
            raise TypeError("Email must be a string")
        
        if "@" not  in value or "." not in value.split("@")[-1]:
            raise ValueError("Invalid email foramt")
        self.__email = value

    @property
    def is_admin(self):
        return self.__is_admin
    
    @is_admin.setter
        def is_admin(self, value):
            if not isinstance(value, bool):
                raise TypeError("is_admin must be a boolean")
        self.__is_admin = value
