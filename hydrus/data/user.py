"""File operations for User authorization."""

from sqlalchemy import exists
from sqlalchemy.orm.exc import NoResultFound
from hydrus.data.exceptions import UserExists, UserNotFound
from hydrus.data.db_models import User
from hashlib import sha224
import random


def add_user(id_, paraphrase, session):
    """Add new users to the database."""
    if session.query(exists().where(User.id == id_)).scalar():
        raise UserExists(id_=id_)
    else:
        new_user = User(id_=id_, paraphrase=paraphrase)
        session.add(new_user)
        session.commit()


def create_nonce(id_, session):
    """Assign a random nonce to the user."""
    user = None
    try:
        user = session.query(User).filter(User.id_ == id_).one()
    except NoResultFound:
        raise UserNotFound(id_=id_)
    user.nonce = random.randint(1, 1000000)
    session.commit()

    return user.nonce


def authenticate_user(id_, hashvalue, session):
    """Authenticate a user based on the nonce and his paraphrase."""
    user = None
    try:
        user = session.query(User).filter(User.id_ == id_).one()
    except NoResultFound:
        raise UserNotFound(id_=id_)
    paraphrase = user.paraphrase
    nonce = str(user.nonce)
    generated_hash = sha224(paraphrase+nonce).hexdigest()

    return generated_hash == hashvalue
