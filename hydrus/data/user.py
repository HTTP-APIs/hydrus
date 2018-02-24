"""File operations for User authorization."""

from sqlalchemy import exists
from sqlalchemy.orm.exc import NoResultFound
from hydrus.data.exceptions import UserExists, UserNotFound
from hydrus.data.db_models import User
from hashlib import sha224
import base64
# import random
from sqlalchemy.orm.session import Session
from werkzeug.local import LocalProxy


def add_user(id_: int, paraphrase: str, session: Session) -> None:
    """Add new users to the database."""
    if session.query(exists().where(User.id == id_)).scalar():
        raise UserExists(id_=id_)
    else:
        new_user = User(id=id_, paraphrase=sha224(paraphrase.encode('utf-8')).hexdigest())
        session.add(new_user)
        session.commit()

# TODO: Implement handhasking for better security
# def create_nonce(id_, session):
#     """Assign a random nonce to the user."""
#     user = None
#     try:
#         user = session.query(User).filter(User.id == id_).one()
#     except NoResultFound:
#         raise UserNotFound(id_=id_)
#     user.nonce = random.randint(1, 1000000)
#     session.commit()
#
#     return user.nonce


def generate_basic_digest(id_: int, paraphrase: str) -> str:
    """Create the digest to be added to the HTTP Authorization header."""
    paraphrase_digest = sha224(paraphrase.encode('utf-8')).hexdigest()
    credentials = str(id_) + ':' + paraphrase_digest
    digest = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    return digest


def authenticate_user(id_: int, paraphrase: str, session: Session) -> bool:
    """Authenticate a user based on the ID and his paraphrase."""
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
    return authenticate_user(auth.username, auth.password, session)