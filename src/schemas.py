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
    done: bool


class ContactStatusUpdate(BaseModel):
    done: bool


class ContactResponse(ContactBase):
    id: int

    class Config:
        orm_mode = True
