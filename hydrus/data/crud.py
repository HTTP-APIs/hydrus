"""Basic CRUD operations for the server."""

from sqlalchemy.orm import sessionmaker, with_polymorphic
from sqlalchemy import exists
from sqlalchemy.exc import IntegrityError
from hydrus.data.db_models import (Graph, BaseProperty, RDFClass, Instance, InstanceProperty, AbstractProperty,
                       Terminal, engine, GraphIAC, GraphIIT, GraphIII)

Session = sessionmaker(bind=engine)
session = Session()
triples = with_polymorphic(Graph, '*')
properties = with_polymorphic(BaseProperty, "*")


def get(id_, session=session):
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


def insert(object_, id_=None, session=session):
    """Insert an object to database [POST] and returns the inserted object."""
    # NOTE: We are inserting the object, no need to check if similar one already exists.
    #       Data can be redundant/identical, they must have different "@id"

    # Added the keymap to generator, no need to use here
    if id_ is not None:
        if session.query(exists().where(Instance.id == id_)).scalar():
            print("ID already exists, updating the object instead.")
            update(id_, object_)
            # Recreate the instance after deletion if isn't already present
            if session.query(exists().where(Instance.id == id_)).scalar():
                instance = session.query(Instance).filter(Instance.id == id_).one()
            else:
                rdf_class = session.query(RDFClass).filter(RDFClass.name == object_["object"]["category"]).one()
                instance = Instance(name=object_["name"], id=id_, type_=rdf_class.id)
                session.add(instance)
                session.commit()
        else:
            try:
                rdf_class = session.query(RDFClass).filter(RDFClass.name == object_["object"]["category"]).one()
                instance = Instance(name=object_["name"], id=id_, type_=rdf_class.id)
                session.add(instance)
                session.commit()
            except IntegrityError:
                return {400: "Instance with ID : %s already exists" % (str(id_))}
    else:
        rdf_class = session.query(RDFClass).filter(RDFClass.name == object_["object"]["category"]).one()
        instance = Instance(name=object_["name"], id=id_, type_=rdf_class.id)
        session.add(instance)
        session.commit()

    triple_store = list()
    try:
        for prop_name in object_["object"]:
            if prop_name != "category":

                # For insertion in IAC
                if session.query(exists().where(RDFClass.name == str(object_["object"][prop_name]))).scalar():
                    if session.query(exists().where(properties.name == prop_name)).scalar():
                        property_ = session.query(properties).filter(properties.name == prop_name).one()
                    else:
                        property_ = BaseProperty(name=prop_name, type_="ABSTRACT")
                        session.add(property_)
                        session.commit()

                    class_name = object_["object"][prop_name]
                    class_ = session.query(RDFClass).filter(RDFClass.name == class_name).one()
                    triple = GraphIAC(subject=instance.id, predicate=property_.id, object_=class_.id)
                    triple_store.append(triple)

                # For insertion in III
                elif session.query(exists().where(Instance.name == str(object_["object"][prop_name]))).scalar():
                    if session.query(exists().where(properties.name == prop_name)).scalar():
                        property_ = session.query(properties).filter(properties.name == prop_name).one()
                    else:
                        property_ = BaseProperty(name=prop_name, type_="ABSTRACT")
                        session.add(property_)
                        session.commit()

                    instance_name = object_["object"][prop_name]
                    instance_object = session.query(Instance).filter(Instance.name == instance_name).one()
                    triple = GraphIII(subject=instance.id, predicate=property_.id, object_=instance_object.id)
                    triple_store.append(triple)
                # For insertion in IIT
                else:
                    # We are not checking for existing terminals as it is highly unlikely two terminals have same value and
                    # this approach allows as to delete unused terminals upon deletion

                    terminal = Terminal(value=object_["object"][prop_name], unit="unit")
                    session.add(terminal)
                    session.commit()
                    if session.query(exists().where(properties.name == prop_name)).scalar():
                        property_ = session.query(properties).filter(properties.name == prop_name).one()
                    else:
                        property_ = BaseProperty(name=prop_name, type_="INSTANCE")
                        session.add(property_)
                        session.commit()

                    triple = GraphIIT(subject=instance.id, predicate=property_.id, object_=terminal.id)
                    triple_store.append(triple)

    except Exception as e:
        print(e)
        session.delete(instance)
        session.commit()
        return {400: "Something went wrong while inserting properties."}

    # Insert everything into database
    session.add_all(triple_store)
    session.commit()
    return instance.id


def delete(id_, session=session):
    """Delete an Instance and all its relations from DB given id [DELETE]."""
    # NOTE: Terminals are reusable, it is part of the reason why they are not stored as literals.
    #       One terminal may map to many different instances in the graph, not advisable to delete them.
    instanceExists = session.query(exists().where(Instance.id == id_)).scalar()
    if instanceExists:
        instance = session.query(Instance).filter(Instance.id == id_)
        data_IIT = session.query(triples).filter(triples.GraphIIT.subject == id_).all()
        data_IAC = session.query(triples).filter(triples.GraphIAC.subject == id_).all()
        data_III = session.query(triples).filter(triples.GraphIII.subject == id_).all()

        data = data_III + data_IIT + data_IAC
        for item in data:
            session.delete(item)
        session.commit()

        instance.delete()
        session.commit()
        # Deleting terminal data as it is highly unlikely that terminals have a same value
        # print("Deleting unused terminals.")
        for data in data_IIT:
            # print(data)
            terminal = session.query(Terminal).filter(Terminal.id == data.object_)
            # session.delete(terminal)
            terminal.delete()
            session.commit()

        return {204: "Object with ID : %s successfully deleted!" % (id_)}
    else:
        return {404: "Instance with ID : %s NOT FOUND" % id_}


def update(id_, object_, session=session):
    """Update an object properties based on the given object [PUT]."""
    instanceExists = session.query(exists().where(Instance.id == id_)).scalar()
    if instanceExists:
        delete(id_)
        insert(object_, id_)
        return {204: "Object with ID : %s successfully updated!" % (id_)}
    else:
        return {404: "Instance with ID : %s NOT FOUND" % id_}


object__ = {
    "name": "12W communication",
    "object": {
        "category": "Spacecraft_Communication",
        "hasMass": 9000,
        "hasMonetaryValue": 4,
        "hasPower": -61,
        "hasVolume": 99,
        "maxWorkingTemperature": 63,
        "minWorkingTemperature": -26
    }
}

# print(update(6, object__))
# print(insert(object__, 6))
# print(delete(6))
# print(update(4, object__))
# print(get(6))
