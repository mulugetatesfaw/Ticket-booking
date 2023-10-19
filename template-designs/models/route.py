from models.base import Base
from models.base import BaseModel
from sqlalchemy import *
from sqlalchemy.orm import * 
from sqlalchemy import ForeignKey
class Route(BaseModel, Base):
    __tablename__ = 'routes'
    date = Column(String(30), nullable = False)
    depcity = Column(String(20), nullable = False)
    descity = Column(String(20), nullable = False)
    kilometer = Column(String(10),nullable = False)
    price = Column(Integer, nullable = False)
    side_no = Column(Integer, nullable = False)
    plate_no = Column(Integer, nullable = False)
    """
    bus_id = Column(String(60), ForeignKey('buses.id'),nullable = False)
    """
    def __init__(self, *args, **kwargs):
        """Initializes City object with super class constructor"""
        super().__init__(*args, **kwargs)
