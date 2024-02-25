from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from fastapi_limiter.depends import RateLimiter

from ..database.db import get_db
from ..database.models import User
from ..schemas import ContactModel, ContactUpdate, ContactResponse
from ..repository import contacts as repository_contacts
from ..services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)
                        ):
    """
    Retrieves a list of contacts.

    Args:
        skip (int, optional): Number of contacts to skip. Defaults to 0.
        limit (int, optional): Maximum number of contacts to return. Defaults to 100.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): Current user. Defaults to Depends(auth_service.get_current_user).

    Returns:
        List[ContactResponse]: List of contacts.
    """
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contact(contact_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieves a single contact by ID.

    Args:
        contact_id (int): ID of the contact to retrieve.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): Current user. Defaults to Depends(auth_service.get_current_user).

    Raises:
        HTTPException: If the contact is not found.

    Returns:
        ContactResponse: The retrieved contact.
    """
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED,
             description='No more than 10 requests per minute',
             dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    Creates a new contact.

    Args:
        body (ContactModel): The contact data.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): Current user. Defaults to Depends(auth_service.get_current_user).

    Returns:
        ContactResponse: The created contact.
    """
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_contact(body: ContactUpdate, contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    Updates an existing contact.

    Args:
        contact_id (int): ID of the contact to update.
        body (ContactUpdate): The updated contact data.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): Current user. Defaults to Depends(auth_service.get_current_user).

    Raises:
        HTTPException: If the contact is not found.

    Returns:
        ContactResponse: The updated contact.
    """
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse,
               description='No more than 10 requests per minute',
               dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    Deletes a contact.

    Args:
        contact_id (int): ID of the contact to delete.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): Current user. Defaults to Depends(auth_service.get_current_user).

    Raises:
        HTTPException: If the contact is not found.

    Returns:
        ContactResponse: The deleted contact.
    """
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/filter/search", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def search_contacts(
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
    name: str = Query(None, title="Name filter",
                      description="Filter contacts by name"),
    surname: str = Query(None, title="Surname filter",
                         description="Filter contacts by surname"),
    email: str = Query(None, title="Email filter",
                       description="Filter contacts by email address"),
    upcoming_birthdays: bool = Query(False, title="Upcoming birthdays",
                                     description="Filter contacts with birthdays in the next 7 days"),
):
    """
    Searches for contacts based on various filters.

    Args:
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): Current user. Defaults to Depends(auth_service.get_current_user).
        name (str, optional): Name filter. Defaults to None.
        surname (str, optional): Surname filter. Defaults to None.
        email (str, optional): Email filter. Defaults to None.
        upcoming_birthdays (bool, optional): Filter for upcoming birthdays. Defaults to False.

    Returns:
        List[ContactResponse]: List of contacts that match the search criteria.
    """
    contacts = await repository_contacts.search_contacts(current_user, db, name=name, surname=surname, email=email,
                                                         upcoming_birthdays=upcoming_birthdays)
    return contacts
