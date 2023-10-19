from models.base import Base
from models.base import BaseModel
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy import ForeignKey
class City(BaseModel, Base):
    __tablename__ = 'cities'
    depcity = Column(String(20), nullable = False)
    def __init__(self, *args, **kwargs):
        """Initializes City object with super class constructor"""
        super().__init__(*args, **kwargs)

