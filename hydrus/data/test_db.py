import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pdb
from db_models import Base, RDFClass


class TestQuery(unittest.TestCase):

    engine = create_engine('sqlite:///test_database.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    def setup(self):
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)

    def teardown(self):
        session.remove()

    ### Will write tests after @chrizandr updates crud.py

if __name__ == '__main__':
    unittest.main()
