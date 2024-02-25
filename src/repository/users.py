from sqlalchemy.orm import Session
from ..database.models import User
from ..schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    Retrieves a user by their email address.

    Args:
        email (str): The email address of the user to retrieve.
        db (Session): The database session.

    Returns:
        User: The User object if found, else None.
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    Creates a new user.

    Args:
        body (UserModel): The UserModel object containing user data.
        db (Session): The database session.

    Returns:
        User: The newly created User object.
    """
    new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    Updates the refresh token for a user.

    Args:
        user (User): The user for whom to update the token.
        token (str, optional): The new refresh token.
        db (Session): The database session.
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    Confirms the email address of a user.

    Args:
        email (str): The email address to confirm.
        db (Session): The database session.
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    """
    Updates the avatar URL for a user.

    Args:
        email (str): The email address of the user.
        url (str): The new avatar URL.
        db (Session): The database session.

    Returns:
        User: The updated User object if found, else None.
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
