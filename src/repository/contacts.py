from typing import List
from sqlalchemy import and_, extract
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from src.database.models import Contact
from src.schemas import ContactModel, ContactUpdate


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(name=body.name, last_name=body.last_name, email=body.email, phone_number=body.phone_number,
                      date_of_birth=body.date_of_birth, additional_data=body.additional_data)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactUpdate, db: Session) -> Contact:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.name = body.name,
        contact.last_name = body.last_name,
        contact.email = body.email,
        contact.phone_number = body.phone_number,
        contact.date_of_birth = body.date_of_birth,
        contact.additional_data = body.additional_data
        db.commit()
    return contact


async def search_contacts(db: Session, name: str = None, surname: str = None, email: str = None,
                          upcoming_birthdays: bool = False) -> List[Contact]:

    query = db.query(Contact)

    if name:
        query = query.filter(and_(Contact.name.ilike(f"%{name}%")))
    if surname:
        query = query.filter(and_(Contact.last_name.ilike(f"%{surname}%")))
    if email:
        query = query.filter(and_(Contact.email.ilike(f"%{email}%")))
    if upcoming_birthdays:
        today = datetime.now().date()
        next_week = today + timedelta(days=7)
        query = query.filter(
            and_(
                extract('month', Contact.date_of_birth) == today.month,
                extract('day', Contact.date_of_birth) >= today.day,
                extract('month', Contact.date_of_birth) == next_week.month,
                extract('day', Contact.date_of_birth) <= next_week.day))
    contacts = query.all()
    return contacts
