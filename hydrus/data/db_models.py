"""Models for Hydra Classes."""

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///database.db')

Base = declarative_base()


class RDFClass(Base):
    """Model for Classes.

    Classes are RDF-OWL or RDF-HYDRA classes.
    """

    __tablename__ = "classes"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        """Verbose object name."""
        return "<id='%s', name='%s'>" % (self.id, self.name)


class Instance(Base):
    """Model for Object/Resource.

    Instances are instances of some kind/classes that are served through the API.
    """

    __tablename__ = "instances"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type_ = Column(Integer, ForeignKey("classes.id"), nullable=True)


class BaseProperty(Base):
    """Model for Basic Property."""

    __tablename__ = "property"

    id = Column(Integer, primary_key=True)
    type = Column(String)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'PROPERTY'
    }

    def __repr__(self):
        """Verbose object name."""
        return "<id='%s', name='%s', type_='%s'>" % (self.id, self.name)


class InstanceProperty(BaseProperty):
    """Model for Instance Properties.

    Instance Properties are properties that are used as predicate when the subject is an Instance.
    >>> prop1 = Property('hasWeight')
    >>> prop2 = Property('hasCost')
    """

    name = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'INSTANCE'
    }

    def __repr__(self):
        """Verbose object name."""
        return "<id='%s', name='%s', type_='%s'>" % (self.id, self.name, self.type)


class AbstractProperty(BaseProperty):
    """Model for Abstract Properties.

    Abstract Properties are properties that are used as predicate between two RDF-OWL classes.
    >>> prop1 = Property('hasWeight')
    >>> prop2 = Property('hasCost')
    Example of a triple:
     RDFClass('A') Property('isSubSystemOf') RDFClass('B')
    """

    name = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'ABSTRACT'
    }

    def __repr__(self):
        """Verbose object name."""
        return "<id='%s', name='%s', type_='%s'>" % (self.id, self.name, self.type)


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

    def __repr__(self):
        """Verbose object name."""
        return "<id='%s', value='%s', unit='%s'>" % (self.id, self.value, self.unit)


class Graph(Base):
    """Model for a graph that store triples of instance from the other models to map relationships."""

    __tablename__ = "graph"

    id = Column(Integer, primary_key=True)
    type = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'Graph',
        'polymorphic_on': type
    }


class GraphCAC(Graph):
    """Graph model for Class >> AbstractProperty >> Class."""

    __tablename__ = 'graphcac'
    subject = Column(Integer, ForeignKey("classes.id"))
    predicate = Column(Integer, ForeignKey("property.id"))
    object = Column(Integer, ForeignKey("classes.id"))

    __mapper_args__ = {
        'polymorphic_identity': 'graphcac',
    }

    def __repr__(self):
        """Verbose object name."""
        return "<subject='%s', predicate='%s', object_='%s'>" % (self.subject, self.predicate, self.object)


class GraphIAC(Graph):
    """Graph model for Instance >> AbstractProperty >> Class."""

    __tablename__ = 'graphiac'
    subject = Column(Integer, ForeignKey("instances.id"))
    predicate = Column(Integer, ForeignKey("property.id"))
    object = Column(Integer, ForeignKey("classes.id"))

    __mapper_args__ = {
        'polymorphic_identity': 'graphiac',
    }

    def __repr__(self):
        """Verbose object name."""
        return "<subject='%s', predicate='%s', object_='%s'>" % (self.subject, self.predicate, self.object)


class GraphIII(Graph):
    """Graph model for Instance >> InstanceProperty >> Instance."""

    __tablename__ = 'graphiii'
    subject = Column(Integer, ForeignKey("instances.id"))
    predicate = Column(Integer, ForeignKey("property.id"))
    object = Column(Integer, ForeignKey("instances.id"))

    __mapper_args__ = {
        'polymorphic_identity': 'graphiii',
    }

    def __repr__(self):
        """Verbose object name."""
        return "<subject='%s', predicate='%s', object_='%s'>" % (self.subject, self.predicate, self.object)


class GraphIIT(Graph):
    """Graph model for Instance >> InstanceProperty >> Terminal."""

    __tablename__ = 'graphiii'
    subject = Column(Integer, ForeignKey("instances.id"))
    predicate = Column(Integer, ForeignKey("property.id"))
    object = Column(Integer, ForeignKey("terminals.id"))

    __mapper_args__ = {
        'polymorphic_identity': 'graphiit',
    }

    def __repr__(self):
        """Verbose object name."""
        return "<subject='%s', predicate='%s', object_='%s'>" % (self.subject, self.predicate, self.object)


if __name__ == "__main__":
    print("Creating models....")
    Base.metadata.create_all(engine)
    print("Done")
