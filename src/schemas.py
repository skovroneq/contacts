from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, constr, validator
from datetime import date, datetime


class ContactBase(BaseModel):
    """
    Base model for contact information.

    Attributes:
        name (str): The name of the contact.
        last_name (str): The last name of the contact.
        email (EmailStr): The email address of the contact.
        phone_number (str): The phone number of the contact.
        date_of_birth (date): The date of birth of the contact.
        additional_data (Optional[str]): Additional data about the contact.
    """
    name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    email: EmailStr
    phone_number: str = Field(pattern=r'^\+?[1-9]\d{1,14}$')
    date_of_birth: date
    additional_data: Optional[str] = None

    @validator("date_of_birth")
    def validate_date_of_birth(cls, v):
        """
        Validator to ensure the date of birth is not in the future.

        Args:
            v (date): The date of birth.

        Raises:
            ValueError: If the date of birth is in the future.

        Returns:
            date: The validated date of birth.
        """
        if v > date.today():
            raise ValueError("Date of birth cannot be in the future")
        return v


class ContactModel(ContactBase):
    """
    Model for creating a new contact.

    Inherits:
        ContactBase: Base model for contact information.
    """
    pass


class ContactUpdate(ContactModel):
    """
    Model for updating an existing contact.

    Inherits:
        ContactModel: Model for creating a new contact.
    """
    pass


class ContactResponse(ContactBase):
    """
    Model for response containing contact information.

    Inherits:
        ContactBase: Base model for contact information.

    Attributes:
        id (int): The unique identifier for the contact.

    Config:
        orm_mode (bool): Allows ORM mode for the model.
    """
    id: int

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    """
    Model for user information.

    Attributes:
        username (str): The username of the user.
        email (EmailStr): The email address of the user.
        password (str): The password of the user.
    """
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    """
    Model for user database representation.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user.
        email (EmailStr): The email address of the user.
        created_at (datetime): The timestamp when the user was created.
        avatar (str | None): The URL to the user's avatar image, if available.

    Config:
        orm_mode (bool): Allows ORM mode for the model.
    """
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    avatar: str | None

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    """
    Model for user response.

    Attributes:
        user (UserDb): The user's information.
        detail (str): Details about the response.

    Attributes:
        detail (str): Details about the response.
    """
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    """
    Model for token information.

    Attributes:
        access_token (str): The access token.
        refresh_token (str): The refresh token.
        token_type (str): The token type.

    Attributes:
        token_type (str): The token type.
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    """
     Model for requesting email.

    Attributes:
        email (EmailStr): The email address.
    """
    email: EmailStr
