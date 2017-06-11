"""Basic CRUD operations for the server."""
# NOTE: Needs to be changed according to new data models
import json

from sqlalchemy.orm import sessionmaker, with_polymorphic
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import exists

import pdb

from hydrus.data.db_models import *
from hydrus.data.keymap import classes_keymap as keymap


Session = sessionmaker(bind=engine)
session = Session()
triples = with_polymorphic(Graph, [GraphCAC, GraphIAC, GraphIII, GraphIIT])


pdb.set_trace()
try:
    session.query(exists().where(triples.id==2)).scalar()
except NoResultFound:
    print("Not found")
