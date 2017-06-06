"""Models for Hydra Classes."""

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
# Default username - postgres, password - "  " (Double space), DB - hydra
engine = create_engine("postgresql://postgres:  @localhost:5432/hydra")

Base = declarative_base()


class RDFClass(Base):
    """Model for Classes.

    Classes are RDF-OWL or RDF-HYDRA classes.
    """
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __repr__(self):
        """Verbose object name."""
        return "<id='%s', name='%s'>" % (self.id, self.name)


class Instance(Base):
    """Model for Object/Resource.

    Instances are instances of some kind/classes that are served through the API.
    """
    __tablename__ = "instances"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    type_ = Column(Integer, ForeignKey("classes.id"), nullable=True)

    def __repr__(self):
        """Verbose object name."""
        return "<id='%s', name='%s', type_='%s'>" % (self.id, self.name, self.type_.name)


class Property(Base):
    """Model for Instance Properties.

    Instance Properties are properties that are used as predicate when the subject is an Instance.

    >>> prop1 = Property('hasWeight')
    >>> prop2 = Property('hasCost')
    """
    __tablename__ = "instance_props"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __repr__(self):
        """Verbose object name."""
        return "<id='%s', name='%s', type_='%s'>" % (self.id, self.name, self.type_)


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
    unit = Column(String, nullable=True)

    def __repr__(self):
        """Verbose object name."""
        return "<id='%s', value='%s', unit='%s'>" % (self.id, self.value, self.unit)


class AbstractProperty(Base):
    """Model for Abstract Properties.

    Abstract Properties are properties that are used as predicate between two RDF-OWL classes.

    >>> prop1 = Property('hasWeight')
    >>> prop2 = Property('hasCost')

    Example of a triple:
     RDFClass('A') Property('isSubSystemOf') RDFClass('B')
    """
    __tablename__ = "abstract_props"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __repr__(self):
        """Verbose object name."""
        return "<id='%s', name='%s', type_='%s'>" % (self.id, self.name, self.type_)


# class Supported_Property(Base):
#     """Class for Hydra Supported Properties."""
#
#     __tablename__ = "supported"
#
#     class_id = Column(Integer, ForeignKey("classes.id"))
#     prop_id = Column(Integer, ForeignKey("property.id"))
#
#     def __repr__(self):
#         """Verbose object name."""
#         return "<class_id='%s', prop_id='%s'>" % (self.class_id, self.prop_id)


class Graph(Base):
    """Model for a graph that store triples of instance from the other models to map relationships.

    Graph triple contains subject, predicate, object.

    #TODO: In the beginning we start with a sparse matrix (a lot of null values) but possibly
     we will refactor with a more memory-efficient solution. See issue #9

    #TODO: in the future all the nodes will be indexed using an Hexastore (3!) strategy.
    """
    __tablename__ = "graph"

    id = Column(Integer, primary_key=True)
    # Subject: can be a class or instance
    class_ = Column(Integer, ForeignKey("classes.id"),
                    nullable=True, index=True)
    instance = Column(Integer, ForeignKey(
        "instances.id"), nullable=True, index=True)
    # Predicate: can be instantiated or abstract
    abs_predicate = Column(Integer, ForeignKey(
        "abstract_props.id"), nullable=True, index=True)
    inst_predicate = Column(Integer, ForeignKey(
        "instance_props.id"), nullable=True, index=True)
    # Object: can be a class or a terminal or instance
    abs_object = Column(Integer, ForeignKey(
        "classes.id"), nullable=True, index=True)
    inst_object = Column(Integer, ForeignKey(
        "instances.id"), nullable=True, index=True)
    term_object = Column(Integer, ForeignKey(
        "terminals.id"), nullable=True, index=True)

    def __repr__(self):
        """Verbose object name."""
        # check which values are not None and return the right string
        return "<class_='%s', instance='%s', abs_predicate='%s', inst_predicate='%s', abs_object='%s', inst_object='%s', term_object='%s'>"\
            % (self.class_, self.instance, self.abs_predicate, self.inst_predicate, self.abs_object, self.inst_object, self.term_object)
        # raise NotImplementedError()
        # pass


if __name__ == "__main__":
    print("Creating models....")
    Base.metadata.create_all(engine)
    print("Done")
