"""Basic CRUD operations for the server."""

from db_models import Graph, BaseProperty, RDFClass, Instance, Terminal, engine
from db_models import GraphIAC, GraphIIT, GraphIII
from sqlalchemy.orm import sessionmaker, with_polymorphic
from sqlalchemy import exists
from keymap import classes_keymap as keymap
import json
import pdb

Session = sessionmaker(bind=engine)
session = Session()
triples = with_polymorphic(Graph, '*')
properties = with_polymorphic(BaseProperty, '*')


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
            prop_name = session.query(properties).filter(properties.id == data.predicate).one().abstract_prop_name
            class_name = session.query(RDFClass).filter(RDFClass.id == data.object_).one().name
            object_template["object"][prop_name] = class_name

        for data in data_III:
            prop_name = session.query(properties).filter(properties.id == data.predicate).one().instance_prop_name
            object_ = get(data.object_)     # Recursive call should get the instance needed
            object_template["object"][prop_name] = object_

        for data in data_IIT:
            prop_name = session.query(properties).filter(properties.id == data.predicate).one().instance_prop_name
            terminal = session.query(Terminal).filter(Terminal.id == data.object_).one()
            object_template["object"][prop_name] = terminal.value + " " + terminal.unit

        object_template["name"] = instance.name
        object_template["@id"] = id_

        print(json.dumps(object_template, indent=True, sort_keys=True))
        return object_template
    else:
        return {404: "Instance with ID : %s NOT FOUND" % id_}


def insert(object_):
    """Insert an object to database [POST] and returns the inserted object."""
    # NOTE: We are inserting the object, no need to check if similar one already exists.
    #       Data can be redundant/identical, they must have different "@id"
    triple_store = list()

    instance = Instance(name=object_["name"])
    session.add(instance)
    session.commit()

    for prop_name in object_["object"]:
        isAbstractProperty = session.query(exists().where(properties.abstract_prop_name == prop_name)).scalar()
        isInstanceProperty = session.query(exists().where(properties.instance_prop_name == prop_name)).scalar()
        # Insert a triple with an abstract property >> GraphIAC
        if isAbstractProperty:
            isValidClass = session.query(exists().where(RDFClass.name == object_["object"][prop_name])).scalar()
            if isValidClass:
                prop = session.query(properties).filter(properties.abstract_prop_name == prop_name).one()
                class_ = session.query(RDFClass).filter(RDFClass.name == object_["object"][prop_name]).one()
                triple = GraphIAC(subject=instance.id, predicate=prop.id, object_=class_.id)
                triple_store.append(triple)
            else:
                session.delete(instance)
                session.commit()
                return {400: "The class %s is not a valid/defined RDFClass" % object_["object"]["prop"]}

        # Insert a triple with an instance property
        elif isInstanceProperty:
            # When object is an instance >> GraphIII
            if type(object_["object"][prop]) is dict:
                object_id = object_["object"][prop]["@id"]
                isValidObject = session.query(exists().where(Instance.id == object_id)).scalar()
                if isValidObject:
                    prop = session.query(properties).filter(properties.instance_prop_name == prop_name).one()
                    triple = GraphIII(subject=instance.id, predicate=prop.id, object_=object_id)
                    triple_store.append(triple)
                else:
                    session.delete(instance)
                    session.commit()
                    return {400: "The instance %s is not a valid Instance" % object_id}
            else:
                # NOTE: Add code here to check existing terminals
                terminal = Terminal(value=object_["object"][prop_name], unit="unit")
                session.add(terminal)
                session.commit()
                prop = session.query(properties).filter(properties.abstract_prop_name == prop_name).one()
                triple = GraphIIT(subject=instance.id, predicate=prop.id, object_=terminal.id)
                triple_store.append(triple)
        else:
            session.delete(instance)
            session.commit()
            return {400: "The property %s is not a valid/defined Property" % prop_name}
    # Insert everything into database
    session.add_all(triple_store)
    session.commit()
    return triple.instance


def delete(id):
    """Delete an Instance and all its relations from DB given id [DELETE]."""
    instanceExists = session.query(exists().where(Instance.id == id)).scalar()
    dataExists = session.query(exists().where(triples.subject == id and triples.type != "graphcac")).scalar()

    if instanceExists:
        instance = session.query(Instance).filter(Instance.id == id).one()
        if dataExists:
            objects = session.query(triples).filter(triples.subject.id == id).all()
            [session.delete(triple) for triple in objects]
        session.delete(instance)
        session.commit()

    # NOTE: Terminals are reusable, it is part of the reason why they are not stored as literals.
    #       One terminal may map to many different instances in the graph, not advisable to delete them.

    return {204: "Object with ID : %s successfully deleted!" % (id)}


def update(id, object_):
    """Update an object properties based on the given object [PUT]."""
    triple_store = list()

    graph_data = session.query(Graph).filter(Graph.instance == id)

    rdf_class_name = keymap[object_["object"]["category"]]
    print("Rdf class name", rdf_class_name)
    rdf_class = session.query(RDFClass).filter(RDFClass.name == rdf_class_name).one()

    # Update old instance if required
    try:
        resource = session.query(Instance).filter(Instance.id == graph_data.all()[0].instance).one()
        resource.name = object_["name"]
        session.commit()
    except Exception as e:
        print(e)
        print("Record with ID %s not found" % (id))

    # delete graph entry
    try:
        graph_data.delete()
        session.commit()
    except Exception as e:
        print("Something went wrong while deleting old Records from Graph!")
        print(e)
    # delete old terminal values
    try:
        for data in graph_data:
            if data.term_object is not None:
                term_object = session.query(Terminal).filter(Terminal.id == data.term_object).delete()
        session.commit()
    except Exception as e:
        print("Something went wrong while deleting terminal objects!")
        print(e)
    # Get/Create properties (both abstract and instance type)
    for prop in object_["object"]:
        if prop != "category":
            # test to set property type (if true abstract)
            try:
                # Check if property value is existing class
                abs_test_1 = session.query(exists().where(RDFClass.name == keymap[object_["object"][prop]])).scalar()
                # Check if property value is existing instance
                abs_test_2 = session.query(exists().where(Instance.name == keymap[object_["object"][prop]])).scalar()
            except:
                abs_test_1 = False
                abs_test_2 = False

            # Abstract property test (if true abstract)
            property_abs_test = abs_test_1 or abs_test_2
            if not property_abs_test:
                abstract_property = None
                try:
                    property_ = session.query(Property).filter(Property.name == prop).one()
                except:
                    # pdb.set_trace()
                    property_ = Property(name=prop)
                    session.add(property_)
                    session.commit()
                    # print("Property id", property_.id)
            else:
                property_ = None
                try:
                    abstract_property = session.query(AbstractProperty).filter(AbstractProperty.name == prop).one()
                except:
                    # pdb.set_trace()
                    abstract_property = AbstractProperty(name=prop)
                    session.add(abstract_property)
                    session.commit()
                    # print("Abstract property id", abstract_property.id)

            # Handle objects insertion/retrieval
            # If property is not abstract then object is of type term_object
            if not property_abs_test:
                term_object = Terminal(value=object_["object"][prop], unit="number")
                session.add(term_object)
                session.commit()

                abs_object = None
                inst_object = None
                # print("Terminal object id", term_object.id)

            # If property is of RDFClass type then object is of abs_object type
            elif session.query(exists().where(RDFClass.name == keymap[object_["object"][prop]])).scalar():
                term_object = None
                abs_object = session.query(RDFClass).filter(RDFClass.name == keymap[object_["object"][prop]]).one()
                inst_object = None
                # print("Abstract object id", abs_object.id)
            # Else object is of inst_object type
            else:
                term_object = None
                abs_object = None
                inst_object = session.query(Instance).filter(Instance.name == keymap[object_["object"][prop]]).one()
                # print("Instance property id", inst_object.id)

            # Create a temporary storage for Our Graph
            triple = Graph(
                class_=rdf_class.id,
                instance=resource.id,
                abs_predicate=abstract_property.id if abstract_property is not None else None,
                inst_predicate=property_.id if property_ is not None else None,
                term_object=term_object.id if term_object is not None else None,
                abs_object=abs_object.id if abs_object is not None else None,
                inst_object=inst_object.id if inst_object is not None else None
            )

            triple_store.append(triple)

    # print(triple_store)

    # Insert everything into database
    session.add_all(triple_store)
    session.commit()
    return triple.instance


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
print(get(2))
