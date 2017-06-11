"""Basic CRUD operations for the server."""
import json

from sqlalchemy.orm import sessionmaker, with_polymorphic
from sqlalchemy import exists
from sqlalchemy.exc import IntegrityError
from hydrus.data.db_models import (Graph, BaseProperty, RDFClass, Instance,
                                   Terminal, engine, GraphIAC, GraphIIT, GraphIII)
from hydrus.data.keymap import classes_keymap as keymap

Session = sessionmaker(bind=engine)
session = Session()
triples = with_polymorphic(Graph, '*')
properties = with_polymorphic(BaseProperty, "*")


def get(id_):
    """Retrieve an Instance with given ID from the database [GET]."""
    object_template = {
        "object": {
            },
        "name": "",
        "@id": ""
    }
    instanceExists = session.query(exists().where(Instance.id == id_)).scalar()
    if instanceExists:
        instance = session.query(Instance).filter(Instance.id == id_).one()
        data_IAC = session.query(triples).filter(triples.GraphIAC.subject == id_).all()
        data_III = session.query(triples).filter(triples.GraphIII.subject == id_).all()
        data_IIT = session.query(triples).filter(triples.GraphIIT.subject == id_).all()

        for data in data_IAC:
            prop_name = session.query(properties).filter(properties.id == data.predicate).one().name
            class_name = session.query(RDFClass).filter(RDFClass.id == data.object_).one().name
            object_template["object"][prop_name] = class_name

        for data in data_III:
            prop_name = session.query(properties).filter(properties.id == data.predicate).one().name
            object_ = get(data.object_)     # Recursive call should get the instance needed
            object_template["object"][prop_name] = object_

        for data in data_IIT:
            prop_name = session.query(properties).filter(properties.id == data.predicate).one().name
            terminal = session.query(Terminal).filter(Terminal.id == data.object_).one()
            object_template["object"][prop_name] = terminal.value + " " + terminal.unit

        object_template["name"] = instance.name
        object_template["@id"] = id_

        return object_template
    else:
        return {404: "Instance with ID : %s NOT FOUND" % id_}


def insert(object_, id_=None):
    """Insert an object to database [POST] and returns the inserted object."""
    # NOTE: We are inserting the object, no need to check if similar one already exists.
    #       Data can be redundant/identical, they must have different "@id"
    triple_store = list()
    if id_ is not None:
        try:
            instance = Instance(name=object_["name"], id=id_)
        except IntegrityError:
            return {400: "Instance with ID : %s already exists" % (str(id_))}
    else:
        instance = Instance(name=object_["name"], id=id_)
    session.add(instance)
    session.commit()

    for prop_name in object_["object"]:
        # Check if it is a valid property
        isValidProperty = session.query(exists().where(properties.name == prop_name)).scalar()
        # Handle invalid properties in the data
        if isValidProperty:
            prop = session.query(properties).filter(properties.name == prop_name).one()
            # Check if it INSTANCE or ABSTRACT Property
            if prop.type_ == "ABSTRACT":
                class_name = object_["object"][prop_name]
                isValidClass = session.query(exists().where(RDFClass.name == class_name)).scalar()
                # Check if it is a valid class
                if isValidClass:
                    class_ = session.query(RDFClass).filter(RDFClass.name == class_name).one()
                    triple = GraphIAC(subject=instance.id, predicate=prop.id, object_=class_.id)
                    triple_store.append(triple)
                # Handle invalid classes
                else:
                    session.delete(instance)
                    session.commit()
                    return {400: "The class %s is not a valid/defined RDFClass" % object_["object"][prop_name]}

            # Insert a triple with an instance property
            elif prop.type_ == "INSTANCE":
                # When object is an instance >> GraphIII
                if type(object_["object"][prop_name]) is dict:
                    object_id = object_["object"][prop_name]["@id"]
                    isValidObject = session.query(exists().where(Instance.id == object_id)).scalar()
                    if isValidObject:
                        triple = GraphIII(subject=instance.id, predicate=prop.id, object_=object_id)
                        triple_store.append(triple)
                    else:
                        session.delete(instance)
                        session.commit()
                        return {400: "The instance %s is not a valid Instance" % object_id}
                # When object is a terminal >> GraphIIT
                else:
                    # NOTE: Add code here to check existing terminals
                    terminal = Terminal(value=object_["object"][prop_name], unit="unit")
                    session.add(terminal)
                    session.commit()
                    triple = GraphIIT(subject=instance.id, predicate=prop.id, object_=terminal.id)
                    triple_store.append(triple)
        else:
            session.delete(instance)
            session.commit()
            return {400: "The property %s is not a valid/defined Property" % prop_name}
    # Insert everything into database
    session.add_all(triple_store)
    session.commit()
    return instance.id


def delete(id_):
    """Delete an Instance and all its relations from DB given id [DELETE]."""
    # NOTE: Terminals are reusable, it is part of the reason why they are not stored as literals.
    #       One terminal may map to many different instances in the graph, not advisable to delete them.
    instanceExists = session.query(exists().where(Instance.id == id_)).scalar()
    if instanceExists:
        instance = session.query(Instance).filter(Instance.id == id_).one()
        data_IIT = session.query(triples).filter(triples.GraphIIT.subject == id_).all()
        data_IAC = session.query(triples).filter(triples.GraphIAC.subject == id_).all()
        data_III = session.query(triples).filter(triples.GraphIII.subject == id_).all()
        data = data_III + data_IAC + data_IIT
        [session.delete(triple) for triple in data]
        session.delete(instance)
        session.commit()
        return {204: "Object with ID : %s successfully deleted!" % (id_)}
    else:
        return {404: "Instance with ID : %s NOT FOUND" % id_}


def update(id_, object_):
    """Update an object properties based on the given object [PUT]."""
    instanceExists = session.query(exists().where(Instance.id == id_)).scalar()
    if instanceExists:
        delete(id_)
        insert(object_, id_)
        return {204: "Object with ID : %s successfully updated!" % (id_)}
    else:
        return {404: "Instance with ID : %s NOT FOUND" % id_}


object__ = {
    'object': {
        'category': 'thermal',
        'minWorkingTemperature': -73,
        'maxWorkingTemperature': 47,
        'hasPower': 0,
        'hasMonetaryValue': 4545,
        'hasVolume': 72,
        'hasMass': 77
        },
    'name': '9KV structure'
}
# print(update(7, object__))
# print(insert(object__))
# print(update(4, object__))
# print(get(4))
