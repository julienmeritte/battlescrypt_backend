from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.internal.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer , primary_key=True , index=True)
    name = Column(String)
    username = Column(String)
    password = Column(String)
    mail = Column(String , unique=True , index=True)
    role = Column(Integer)