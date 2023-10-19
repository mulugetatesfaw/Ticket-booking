from sqlalchemy import *
from models.base import BaseModel, Base
from sqlalchemy.orm import *

class Bus(BaseModel, Base):
    __tablename__ = 'buses'
    plate_no = Column(Integer,nullable=False,unique=True)
    sideno = Column(Integer,nullable=False,unique=True)
    no_seats = Column(Integer,nullable=False)
    
    """ routeid = relationship("Route", backref="buses")"""
    """tickets = relationship("Ticket", backref="buses")"""

    """tickets = relationship("Ticket", backref="buses")"""

    def __init__(self, *args, **kwargs):
        """Initializes City object with super class constructor"""
        super().__init__(*args, **kwargs)
