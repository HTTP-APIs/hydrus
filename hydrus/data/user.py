"""File operations for User authorization."""

from sqlalchemy import exists
from sqlalchemy.orm.exc import NoResultFound
from hydrus.data.exceptions import UserExists, UserNotFound
from hydrus.data.db_models import User, Token, Nonce
from hashlib import sha224
import base64
# import random
from sqlalchemy.orm.session import Session
from werkzeug.local import LocalProxy
from random import randrange
from datetime import datetime, timedelta
from uuid import uuid4


def add_user(id_: int, paraphrase: str, session: Session) -> None:
    """Add new users to the database.

    Raises:
        UserExits: If a user with `id_` already exists.

    """
    if session.query(exists().where(User.id == id_)).scalar():
        raise UserExists(id_=id_)
    else:
        new_user = User(id=id_, paraphrase=sha224(
            paraphrase.encode('utf-8')).hexdigest())
        session.add(new_user)
        session.commit()


def check_nonce(request: LocalProxy, session: Session) -> bool:
    """check validity of nonce passed by the user."""
    try:
        id_ = request.headers['X-Authentication']
        nonce = session.query(Nonce).filter(Nonce.id == id_).one()
        present = datetime.now()
        present = present - nonce.timestamp
        session.delete(nonce)
        session.commit()
        if present > timedelta(0, 0, 0, 0, 1, 0, 0):
            return False
    except BaseException:
        return False
    return True


def create_nonce(session: Session) -> str:
    """
    Create a one time use nonce valid for a short time
    for user authentication.
    """
    nonce = str(uuid4())
    time = datetime.now()
    new_nonce = Nonce(id=nonce, timestamp=time)
    session.add(new_nonce)
    session.commit()
    return nonce


def add_token(request: LocalProxy, session: Session) -> str:
    """
    Create a new token for the user or return a
    valid existing token to the user.
    """
    token = None
    id_ = int(request.authorization['username'])
    try:
        token = session.query(Token).filter(Token.user_id == id_).one()
        if not token.is_valid():
            update_token = '%030x' % randrange(16**30)
            token.id = update_token
            token.timestamp = datetime.now()
            session.commit()
    except NoResultFound:
        token = '%030x' % randrange(16**30)
        new_token = Token(user_id=id_, id=token)
        session.add(new_token)
        session.commit()
        return token
    return token.id


def check_token(request: LocalProxy, session: Session) -> bool:
    """
    check validity of the token passed by the user.
    """
    token = None
    try:
        id_ = request.headers['X-Authorization']
        token = session.query(Token).filter(Token.id == id_).one()
        if not token.is_valid():
            token.delete()
            return False
    except BaseException:
        return False
    return True


def generate_basic_digest(id_: int, paraphrase: str) -> str:
    """Create the digest to be added to the HTTP Authorization header."""
    paraphrase_digest = sha224(paraphrase.encode('utf-8')).hexdigest()
    credentials = '{}:{}'.format(id_, paraphrase_digest)
    digest = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    return digest


def authenticate_user(id_: int, paraphrase: str, session: Session) -> bool:
    """Authenticate a user based on the ID and his paraphrase.

    Raises:
        UserNotFound: If a user with `id_` is not a valid/defined User

    """
    user = None
    try:
        user = session.query(User).filter(User.id == id_).one()
    except NoResultFound:
        raise UserNotFound(id_=id_)
    hashvalue = user.paraphrase
    generated_hash = sha224(paraphrase.encode('utf-8')).hexdigest()

    return generated_hash == hashvalue


def check_authorization(request: LocalProxy, session: Session) -> bool:
    """Check if the request object has the correct authorization."""
    auth = request.authorization
    if check_nonce(request, session):
        return authenticate_user(auth.username, auth.password, session)
    return False
