from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    last_name = Column(String(50))
    email = Column(String, unique=True)
    phone_number = Column(String)
    date_of_birth = Column(Date)
    additional_data = Column(String, nullable=True)
