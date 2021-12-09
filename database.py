from sqlalchemy import (
    Column, 
    Integer,
    String,
    DateTime,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

class Metadata(Base):
    __tablename__ = 'metadata'
    id = Column(Integer, primary_key=True)
    file_name = Column(String, nullable=False, unique=True)
    owner = Column(String, nullable=False)
    uploaded_date = Column(DateTime, nullable=False)
