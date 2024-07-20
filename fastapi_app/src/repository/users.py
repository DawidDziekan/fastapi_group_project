from libgravatar import Gravatar
from sqlalchemy.orm import Session

from fastapi_app.src.database.models import User
from fastapi_app.src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    Retrieves a user by their email.

    :param email: The email address of the user.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: The user object if found, otherwise None.
    :rtype: User
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    Creates a new user.

    :param body: The user registration details.
    :type body: UserModel
    :param db: The database session.
    :type db: Session
    :return: The newly created user object.
    :rtype: User
    :raises Exception: If an error occurs while fetching the Gravatar image.
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
        
    if db.query(User).count() == 0:
        role = "admin"
    else:
        role = "user"
        
    new_user = User(**body.dict(), avatar = avatar, role = role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    Updates the refresh token for a user.

    :param user: The user object.
    :type user: User
    :param token: The new refresh token, or None to clear it.
    :type token: str | None
    :param db: The database session.
    :type db: Session
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    Confirms a user's email address.

    :param email: The email address to be confirmed.
    :type email: str
    :param db: The database session.
    :type db: Session
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    """
    Updates the avatar URL for a user.

    :param email: The email address of the user.
    :type email: str
    :param url: The new avatar URL.
    :type url: str
    :param db: The database session.
    :type db: Session
    :return: The updated user object.
    :rtype: User
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
