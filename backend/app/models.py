from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Donor(Base):
    __tablename__ = "donors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    blood_group = Column(String)
    phone_number = Column(String, unique=True, index=True) 
    
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    city = Column(String, default="Ranchi")

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    blood_group = Column(String)
    phone_number = Column(String, unique=True, index=True)
    
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    city = Column(String, default="Ranchi")
    
    symptoms = Column(String, nullable=True)