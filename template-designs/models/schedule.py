from sqlalchemy import *
from models.base import Base, BaseModel



class Schedule(Base, BaseModel):
    __tablename__ = 'schedules'
    plate_no = Column(Integer,nullable=False, unique = True)
    depcity = Column(String(30),nullable = False)
    descity = Column(String(30),nullable = False)
    kilometer = Column(Float(7),nullable = False)
    price = Column(Float(6),nullable = False)


