"""Basic CRUD operations for the server."""

from sqlalchemy.orm import sessionmaker, with_polymorphic
from sqlalchemy import exists
from sqlalchemy.orm.exc import NoResultFound
from hydrus.data.db_models import (Graph, BaseProperty, RDFClass, Instance,
                                   Terminal, engine, GraphIAC, GraphIIT, GraphIII)
Session = sessionmaker(bind=engine)
session = Session()
triples = with_polymorphic(Graph, '*')
properties = with_polymorphic(BaseProperty, "*")


def get(id_, type_, session=session):
    """Retrieve an Instance with given ID from the database [GET]."""
    object_template = {
        "object": {
        },
        "name": "",
        "@id": "",
        "@type": "",
    }
    try:
        rdf_class = session.query(RDFClass).filter(
            RDFClass.name == type_).one()
    except NoResultFound:
        return {400: "The class %s is not a valid/defined RDFClass" % type_}

    try:
        instance = session.query(Instance).filter(
            Instance.id == id_, Instance.type_ == rdf_class.id).one()
    except NoResultFound:
        return {404: "Instance with ID : %s of Type : %s, NOT FOUND" % (id_, type_)}

    data_IAC = session.query(triples).filter(
        triples.GraphIAC.subject == id_).all()
    data_III = session.query(triples).filter(
        triples.GraphIII.subject == id_).all()
    data_IIT = session.query(triples).filter(
        triples.GraphIIT.subject == id_).all()

    for data in data_IAC:
        prop_name = session.query(properties).filter(
            properties.id == data.predicate).one().name
        class_name = session.query(RDFClass).filter(
            RDFClass.id == data.object_).one().name
        object_template["object"][prop_name] = class_name

    for data in data_III:
        prop_name = session.query(properties).filter(
            properties.id == data.predicate).one().name
        instance = session.query(Instance).filter(
            Instance.id == data.object_).one()
        # Recursive call should get the instance needed
        object_ = get(id_=instance.id, type_=instance.type_, session=session)
        object_template["object"][prop_name] = object_

    for data in data_IIT:
        prop_name = session.query(properties).filter(
            properties.id == data.predicate).one().name
        terminal = session.query(Terminal).filter(
            Terminal.id == data.object_).one()
        object_template["object"][prop_name] = terminal.value + \
            " " + terminal.unit

    object_template["name"] = instance.name
    object_template["@id"] = "/api/" + type_ + "/" + str(id_)
    object_template["@type"] = rdf_class.name

    return object_template


def insert(object_, id_=None, session=session):
    """Insert an object to database [POST] and returns the inserted object."""
    rdf_class = None
    instance = None

    # Check for class in the begging
    try:
        rdf_class = session.query(RDFClass).filter(
            RDFClass.name == object_["@type"]).one()
    except NoResultFound:
        return {400: "The class %s is not a valid/defined RDFClass" % object_["@type"]}

    if id_ is not None:
        # Update the object if ID already exists
        if session.query(exists().where(Instance.id == id_)).scalar():
            # return update(id_, object_)   # Updates should be using PUT not POST
            return {400: "Instance with ID : %s already exists" % str(id_)}

        instance = Instance(name=object_["name"], id=id_, type_=rdf_class.id)
    else:
        instance = Instance(name=object_["name"], type_=rdf_class.id)

    session.add(instance)
    session.commit()

    for prop_name in object_["object"]:
        # NOTE: An instance would have to be a JSON object, not string. Otherwise we may have an instance named 23 which will be added
        #  everytime the number is used. Use instance = {"@id": 2 }, where 2 is the ID of the instance.
        try:
            property_ = session.query(properties).filter(
                properties.name == prop_name).one()
        except NoResultFound:
            # Adds new Property
            property_ = BaseProperty(name=prop_name)
            session.add(property_)
            session.flush()
            # @xadahiya, if you comment the above lines and uncomment these, it will use only the properties in DB
            # session.close()
            # session.delete(instance)
            # session.commit()
            # return {400: "%s is not a defined Property" % prop_name}

        # For insertion in III
        if type(object_["object"][prop_name]) == dict:
            try:
                instance_id = object_["object"][prop_name]["@id"]
                instance_object = session.query(Instance).filter(
                    Instance.id == instance_id).one()
            except (KeyError, NoResultFound) as e:
                print(e)
                session.close()
                session.delete(instance)
                session.commit()
                return {400: "The instance for %s is not valid" % prop_name}

            if property_.type_ == "PROPERTY" or property_.type_ == "INSTANCE":
                property_.type_ = "INSTANCE"
                session.add(property_)
                triple = GraphIII(
                    subject=instance.id, predicate=property_.id, object_=instance_object.id)
                # Add things directly to session, if anything fails whole transaction is aborted
                session.add(triple)
            else:
                session.close()
                session.delete(instance)
                session.commit()
                return {400: "%s is not an Instance Property" % prop_name}

        else:
            # For insertion in IAC
            if session.query(exists().where(RDFClass.name == str(object_["object"][prop_name]))).scalar():
                if property_.type_ == "PROPERTY" or property_.type_ == "ABSTRACT":
                    property_.type_ = "ABSTRACT"
                    session.add(property_)
                    class_ = session.query(RDFClass).filter(
                        RDFClass.name == object_["object"][prop_name]).one()
                    triple = GraphIAC(subject=instance.id,
                                      predicate=property_.id, object_=class_.id)
                    session.add(triple)
                else:
                    session.close()
                    session.delete(instance)
                    session.commit()
                    return {400: "%s is not an Abstract Property" % prop_name}

            # For insertion in IIT
            else:
                terminal = Terminal(
                    value=object_["object"][prop_name], unit="unit")
                session.add(terminal)
                session.flush()     # Assigns ID without committing

                if property_.type_ == "PROPERTY" or property_.type_ == "INSTANCE":
                    property_.type_ = "INSTANCE"
                    session.add(property_)
                    triple = GraphIIT(
                        subject=instance.id, predicate=property_.id, object_=terminal.id)
                    # Add things directly to session, if anything fails whole transaction is aborted
                    session.add(triple)
                else:
                    session.close()
                    session.delete(instance)
                    session.commit()
                    return {400: "%s is not an Instance Property" % prop_name}

    session.commit()
    # pdb.set_trace()
    return {201: "Object with id %s successfully added!" % (instance.id)}


def delete(id_, type_, session=session):
    """Delete an Instance and all its relations from DB given id [DELETE]."""
    try:
        rdf_class = session.query(RDFClass).filter(
            RDFClass.name == type_).one()
    except NoResultFound:
        return {400: "The class %s is not a valid/defined RDFClass" % type_}
    try:
        instance = session.query(Instance).filter(
            Instance.id == id_ and type_ == rdf_class.id).one()
    except NoResultFound:
        return {404: "Instance with ID : %s and Type : %s, NOT FOUND" % (id_, type_)}

    data_IIT = session.query(triples).filter(
        triples.GraphIIT.subject == id_).all()
    data_IAC = session.query(triples).filter(
        triples.GraphIAC.subject == id_).all()
    data_III = session.query(triples).filter(
        triples.GraphIII.subject == id_).all()

    data = data_III + data_IIT + data_IAC
    for item in data:
        session.delete(item)

    for data in data_IIT:
        terminal = session.query(Terminal).filter(
            Terminal.id == data.object_).one()
        session.delete(terminal)

    session.delete(instance)
    session.commit()
    return {200: "Object with ID : %s successfully deleted!" % (id_)}


def update(id_, type_, object_, session=session):
    """Update an object properties based on the given object [PUT]."""
    # Keep the object as fail safe
    instance = get(id_, type_, session)
    if "object" in instance:
        instance.pop("@id")
        # Try deleteing the object
        delete_status = delete(id_=id_, type_=type_, session=session)
        if 200 in delete_status:
            # Try inserting the new data
            insert_status = insert(object_=object_, id_=id_, session=session)
            if 200 in insert_status:
                return {200: "Object with ID : %s successfully updated!" % (id_)}
            else:
                return insert_status
        else:
            return delete_status
    else:
        return {400: "Something went wrong, try again."}


def get_collection(type_, session=session):
    """Retrieve a type of collection from the database."""
    collection_template = {
        "@id": "/api/" + type_ + "/",
        "@context": None,
        "@type": type_ + "Collection",
        "members": []
    }
    try:
        rdf_class = session.query(RDFClass).filter(
            RDFClass.name == type_).one()
    except NoResultFound:
        return {400: "The class %s is not a valid/defined RDFClass" % type_}

    try:
        instances = session.query(Instance).filter(
            Instance.type_ == rdf_class.id).all()
    except NoResultFound:
        instances = []
        return {404: "Instance with ID : %s of Type : %s, NOT FOUND" % (id_, type_)}

    if len(instances) > 0:
        for instance_ in instances:
            object_template = {
                "@id": "/api/" + type_ + "/" + str(instance_.id),
                "@type": type_

            }
            collection_template["members"].append(object_template)
    return collection_template

    object__ = {
        "name": "12W communication",
        "@type": "Spacecraft_Communication",
        "object": {
            "hasMass": 9000,
            "hasMonetaryValue": 4,
            "hasPower": -61,
            "hasVolume": 99,
            "maxWorkingTemperature": 63,
            "minWorkingTemperature": -26
        }
    }


object_2 = {'name': 'Not defined :p', '@type': 'Order', 'object': {'Speed': '2334', 'Destination': 'india'},
            '@context': {'Speed': 'http://auto.schema.org/speed', 'Destination': 'http://schema.org/geo'}}

if __name__ == "__main__":
    # print(update(6, object__))
    print(insert(object_2))
    # print(delete(1))
    # print(update(4, object__))
    # print(get(1, "Spacecraft_Communication"))
    # print(get_collection("Spacecraft_Communication"))
