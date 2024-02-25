from sqlalchemy import Column, Integer, String, Date, func, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contact(Base):
    """
    Represents a contact entity in the database.

    Attributes:
        id (int): The primary key identifier for the contact.
        name (str): The name of the contact.
        last_name (str, optional): The last name of the contact.
        email (str, unique): The email address of the contact.
        phone_number (str): The phone number of the contact.
        date_of_birth (datetime.date, optional): The date of birth of the contact.
        additional_data (str, optional): Additional data related to the contact.
        user_id (int, optional): The foreign key referencing the associated user.
        user (User, optional): The relationship to the associated user entity.
    """
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    last_name = Column(String(50))
    email = Column(String, unique=True)
    phone_number = Column(String)
    date_of_birth = Column(Date)
    additional_data = Column(String, nullable=True)
    user_id = Column('user_id', ForeignKey(
        'users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="contacts")


class User(Base):
    """
    Represents a user entity in the database.

    Attributes:
        id (int): The primary key identifier for the user.
        username (str): The username of the user.
        email (str, unique): The email address of the user.
        password (str): The password hash of the user.
        created_at (datetime.datetime): The timestamp when the user was created.
        avatar (str, optional): The URL to the user's avatar image.
        refresh_token (str, optional): The refresh token used for authentication.
        confirmed (bool): Indicates if the user's email address has been confirmed.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
