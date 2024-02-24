from typing import List
from sqlalchemy import and_, extract
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..database.models import Contact, User
from ..schemas import ContactModel, ContactUpdate


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts for a particular user.

    Args:
        skip (int): The number of contacts to skip.
        limit (int): The maximum number of contacts to return.
        user (User): The user for whom contacts are retrieved.
        db (Session): The database session.

    Returns:
        List[Contact]: A list of Contact objects filtered by the specified user ID.
    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    """
    Retrieves a single contact by its ID for a particular user.

    Args:
        contact_id (int): The ID of the contact to retrieve.
        user (User): The user who owns the contact.
        db (Session): The database session.

    Returns:
        Contact: The Contact object with the specified ID and associated with the specified user.
    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    """
    Creates a new contact for the particular user.

    Args:
        body (ContactModel): The data for the new contact.
        user (User): The user who owns the contact.
        db (Session): The database session.

    Returns:
        Contact: The newly created Contact object.
    """
    contact = Contact(
        name=body.name,
        last_name=body.last_name,
        email=body.email,
        phone_number=body.phone_number,
        date_of_birth=body.date_of_birth,
        additional_data=body.additional_data,
        user_id=user.id
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact:
    """
    Removes a contact associated with the particular user.

    Args:
        contact_id (int): The ID of the contact to remove.
        user (User): The user who owns the contact.
        db (Session): The database session.

    Returns:
        Contact: The removed Contact object, or None if the contact does not exist.
    """
    contact = db.query(Contact).filter(
        and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactUpdate, user: User, db: Session) -> Contact:
    """
     Updates a contact associated with the particular user.

    Args:
        contact_id (int): The ID of the contact to update.
        body (ContactUpdate): The data to update the contact with.
        user (User): The user who owns the contact.
        db (Session): The database session.

    Returns:
        Contact: The updated Contact object, or None if the contact does not exist.
    """
    contact = db.query(Contact).filter(
        and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.name = body.name,
        contact.last_name = body.last_name,
        contact.email = body.email,
        contact.phone_number = body.phone_number,
        contact.date_of_birth = body.date_of_birth,
        contact.additional_data = body.additional_data
        db.commit()
    return contact


async def search_contacts(user: User, db: Session, name: str = None, surname: str = None, email: str = None,
                          upcoming_birthdays: bool = False) -> List[Contact]:
    """
    Searches contacts associated with the particular user based on provided criteria.

    Args:
        user (User): The user to search contacts for.
        db (Session): The database session.
        name (str, optional): The name to search for.
        surname (str, optional): The surname to search for.
        email (str, optional): The email to search for.
        upcoming_birthdays (bool, optional): Whether to search for contacts with upcoming birthdays.

    Returns:
        List[Contact]: A list of Contact objects that match the search criteria.
    """
    query = db.query(Contact).filter(Contact.user_id == user.id)

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
