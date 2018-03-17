"""Models for Hydra Classes."""

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from typing import Any
# from hydrus.settings import DB_URL

engine = create_engine('sqlite:///database.db')

Base = declarative_base() # type: Any


class RDFClass(Base):
    """Model for Classes.
    Classes are RDF-OWL or RDF-HYDRA classes.
    """

    __tablename__ = "classes"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __repr__(self) -> str:
        """Verbose object name."""
        return "<id='%s', name='%s'>" % (self.id, self.name)


class Instance(Base):
    """Model for Object/Resource.
    Instances are instances of some kind/classes that are served through the API.
    """

    __tablename__ = "instances"

    id = Column(Integer, primary_key=True)
    type_ = Column(Integer, ForeignKey("classes.id"), nullable=True)


class BaseProperty(Base):
    """Model for Basic Property."""

    __tablename__ = "property"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    type_ = Column(String)

    __mapper_args__ = {
        'polymorphic_on': type_,
        'polymorphic_identity': 'PROPERTY'
    }


class InstanceProperty(BaseProperty):
    """Model for Instance Properties.
    Instance Properties are properties that are used as predicate when the subject is an Instance.
    >>> prop1 = BaseProperty('hasWeight')
    >>> prop2 = BaseProperty('hasCost')
    """

    __mapper_args__ = {
        'polymorphic_identity': 'INSTANCE'
    }

    def __repr__(self) -> str:
        """Verbose object name."""
        return "<id='%s', name='%s', type='%s'>" % (self.id, self.name, self.type_)


class AbstractProperty(BaseProperty):
    """Model for Abstract Properties.
    Abstract Properties are properties that are used as predicate between two RDF-OWL classes.
    >>> prop1 = BaseProperty('hasWeight')
    >>> prop2 = BaseProperty('hasCost')
    Example of a triple:
     RDFClass('A') Property('isSubSystemOf') RDFClass('B')
    """

    __mapper_args__ = {
        'polymorphic_identity': 'ABSTRACT'
    }

    def __repr__(self) -> str:
        """Verbose object name."""
        return "<id='%s', name='%s', type='%s'>" % (self.id, self.name, self.type_)


class Terminal(Base):
    """Model for Terminals.
    Terminals are numbers or string that can be referenced by a Property. They can be only
     objects in a triple.
    >>> t = Terminal(value=85, unit='cubic centimeters')
    >>> t1 = Terminal(value='Cubesat', unit='standard')
    """

    __tablename__ = "terminals"

    id = Column(Integer, primary_key=True)
    value = Column(String)
    unit = Column(String)

    def __repr__(self) -> str:
        """Verbose object name."""
        return "<id='%s', value='%s', unit='%s'>" % (self.id, self.value, self.unit)


class Graph(Base):
    """Model for a graph that store triples of instance from the other models to map relationships."""

    __tablename__ = "graph"

    id = Column(Integer, primary_key=True)
    type = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'graph',
        'polymorphic_on': type
    }


class GraphCAC(Graph):
    """Graph model for Class >> AbstractProperty >> Class."""

    __tablename__ = 'graphcac'
    id = Column(Integer, ForeignKey('graph.id'), primary_key=True)
    subject = Column(Integer, ForeignKey("classes.id"))
    predicate = Column(Integer, ForeignKey("property.id"))
    object_ = Column(Integer, ForeignKey("classes.id"))

    __mapper_args__ = {
        'polymorphic_identity': 'graphcac',
    }

    def __repr__(self) -> str:
        """Verbose object name."""
        return "<subject='%s', predicate='%s', object_='%s'>" % (self.subject, self.predicate, self.object_)


class GraphIAC(Graph):
    """Graph model for Instance >> AbstractProperty >> Class."""

    __tablename__ = 'graphiac'
    id = Column(Integer, ForeignKey('graph.id'), primary_key=True)
    subject = Column(Integer, ForeignKey("instances.id"))
    predicate = Column(Integer, ForeignKey("property.id"))
    object_ = Column(Integer, ForeignKey("classes.id"))

    __mapper_args__ = {
        'polymorphic_identity': 'graphiac',
    }

    def __repr__(self) -> str:
        """Verbose object name."""
        return "<subject='%s', predicate='%s', object_='%s'>" % (self.subject, self.predicate, self.object_)


class GraphIII(Graph):
    """Graph model for Instance >> InstanceProperty >> Instance."""

    __tablename__ = 'graphiii'
    id = Column(Integer, ForeignKey('graph.id'), primary_key=True)
    subject = Column(Integer, ForeignKey("instances.id"))
    predicate = Column(Integer, ForeignKey("property.id"))
    object_ = Column(Integer, ForeignKey("instances.id"))

    __mapper_args__ = {
        'polymorphic_identity': 'graphiii',
    }

    def __repr__(self) -> str:
        """Verbose object name."""
        return "<subject='%s', predicate='%s', object_='%s'>" % (self.subject, self.predicate, self.object_)


class GraphIIT(Graph):
    """Graph model for Instance >> InstanceProperty >> Terminal."""

    __tablename__ = 'graphiit'
    id = Column(Integer, ForeignKey('graph.id'), primary_key=True)
    subject = Column(Integer, ForeignKey("instances.id"))
    predicate = Column(Integer, ForeignKey("property.id"))
    object_ = Column(Integer, ForeignKey("terminals.id"))

    __mapper_args__ = {
        'polymorphic_identity': 'graphiit',
    }

    def __repr__(self) -> str:
        """Verbose object name."""
        return "<subject='%s', predicate='%s', object_='%s'>" % (self.subject, self.predicate, self.object_)


class User(Base):
    """Model for a user that stores the ID, paraphrase and a nonce."""

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    paraphrase = Column(String)

class Token(Base):
    """Model for storing tokens for the users."""

    __tablename__ = "tokens"
    id = Column(String, primary_key = True, index = True)
    user_id = Column(Integer, ForeignKey('user.id'))
    timestamp = Column(DateTime, index = True) 

class Nonce(Base):
    """Model for storing nonce for the users."""

    __tablename__  = "nonce"
    id = Column(String, primary_key = True, index = True)
    timestamp = Column(DateTime, index = True)

if __name__ == "__main__":
    print("Creating models....")
    Base.metadata.create_all(engine)
    print("Done")