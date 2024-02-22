from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, constr, validator
from datetime import date, datetime


class ContactBase(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    email: EmailStr
    phone_number: str = Field(pattern=r'^\+?[1-9]\d{1,14}$')
    date_of_birth: date
    additional_data: Optional[str] = None

    @validator("date_of_birth")
    def validate_date_of_birth(cls, v):
        if v > date.today():
            raise ValueError("Date of birth cannot be in the future")
        return v


class ContactModel(ContactBase):
    pass


class ContactUpdate(ContactModel):
    pass


class ContactResponse(ContactBase):
    id: int

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
