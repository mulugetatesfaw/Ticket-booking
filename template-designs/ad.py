import hashlib
from models.admin import Admin
from models.base import BaseModel

data = [
    {
        "fname": "ananya",
        "lname": "tamre",
        "username": "hello",
        "password": "12345678",  # Encrypted password should be a string
        "phone": 987655444,
        "gender": "male",
        "email": "anany@gmail.com"
    }
]

for d in data:
    p = Admin(**d)
    p.save()

class Admin(BaseModel):
    def __init__(self, *args, **kwargs):
        """Initializes Admin object with super class constructor"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """Sets a password with md5 encryption"""
        if name == "password":
            value = hashlib.md5(value.encode()).hexdigest()
        super().__setattr__(name, value)
