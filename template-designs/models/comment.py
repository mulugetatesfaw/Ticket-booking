from models.base import BaseModel, Base
from sqlalchemy import *
class Fedback(BaseModel,Base):

    __tablename__ = 'comments'
    name = Column(String(30), nullable=False)
    email = Column(String(30), nullable=False)
    phone = Column(Integer, nullable=False)
    message = Column(String(200),nullable=False)

