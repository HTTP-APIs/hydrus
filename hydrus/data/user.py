"""File operations for User authorization."""

from sqlalchemy import exists
from sqlalchemy.orm.exc import NoResultFound
from hydrus.data.exceptions import UserExists, UserNotFound
from hydrus.data.db_models import User,Token
from hashlib import sha224
import base64
# import random
from sqlalchemy.orm.session import Session
from werkzeug.local import LocalProxy
from random import randrange


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

def add_token(request: LocalProxy, session: Session) -> str:
    token = None
    id_ = int(request.authorization['username'])
    try:
        token = session.query(Token).filter(Token.user_id == id_).one()
    except NoResultFound:
        token = '%030x' % randrange(16**30)
        new_token = Token(user_id=id_,id=token)
        session.add(new_token)
        session.commit()
        return token
    return token.id

def check_token(request: LocalProxy, session: Session) -> bool:
    token = None
    try:
        id_ = request.args['token']
        token = session.query(Token).filter(Token.id == id_).one()
    except:
        return False
    return True

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