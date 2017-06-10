"""Basic CRUD operations for the server."""

from db_models import Property, Instance, Graph, engine, RDFClass, Terminal, AbstractProperty
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exists
from keymap import classes_keymap as keymap
import json
# import pdb

Session = sessionmaker(bind=engine)
session = Session()


def get(id):
    """Retrieve a object with instance_id=id from the database [GET]."""
    object_template = {
        "object": {
            "category": "",
            },
        "name": ""
    }

    try:
        graph_data = session.query(Graph).filter(Graph.instance == id).all()
        # print(graph_data)
        instance_name = session.query(Instance).filter(Instance.id == graph_data[0].instance).one().name
        # print(instance_name)
        class_name = session.query(RDFClass).filter(RDFClass.id == graph_data[0].class_).one().name
        properties = []
        for data in graph_data:
            if data.inst_predicate is not None and data.abs_predicate is None:
                prop = session.query(Property).filter(Property.id == data.inst_predicate).one().name
                prop_val = session.query(Terminal).filter(Terminal.id == data.term_object).one().value
            elif data.abs_predicate is not None and data.inst_predicate is None:
                prop = session.query(AbstractProperty).filter(AbstractProperty.id == data.abs_predicate).one().name
                if data.abs_object is not None and data.inst_object is None:
                    prop_val = session.query(RDFClass).filter(RDFClass.id == data.abs_object).one().name
                elif data.inst_object is not None and data.abs_object is None:
                    prop_val = session.query(Instance).filter(Instance.id == data.inst_object).one().name
                else:
                    print("Something went wrong when retrieving property values!")
            else:
                print("Something went wrong when retrieving properties!")

            properties.append((prop, prop_val))

        # print(properties)

        object_template["name"] = str(instance_name)
        for prop, prop_val in properties:
            object_template["object"][str(prop)] = str(prop_val)

        object_template["object"]["category"] = str(class_name)
        # print(json.dumps(object_template, indent=4, sort_keys=True))
        return json.dumps(object_template, indent=4, sort_keys=True)
    except Exception as e:
        print(e)
        return -1

# print(get(3))


def insert(object_):
    """Insert an object to database using Sqlalchemy [Post] and returns the inserted object's ID."""
    # Query and get Rdf class
    triple_store = list()

    rdf_class_name = keymap[object_["object"]["category"]]
    print("Rdf class name", rdf_class_name)
    rdf_class = session.query(RDFClass).filter(RDFClass.name == rdf_class_name).one()

    # Get/Create Instance object
    try:
        resource = session.query(Instance).filter(Instance.name == object_["name"]).one()
    except:
        resource = Instance(name=object_["name"], type_=rdf_class.id)
        session.add(resource)
        session.commit()
    print("Resource id", resource.id)

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
                    print("Property id", property_.id)
            else:
                property_ = None
                try:
                    abstract_property = session.query(AbstractProperty).filter(AbstractProperty.name == prop).one()
                except:
                    # pdb.set_trace()
                    abstract_property = AbstractProperty(name=prop)
                    session.add(abstract_property)
                    session.commit()
                    print("Abstract property id", abstract_property.id)

            # Handle objects insertion/retrieval
            # If property is not abstract then object is of type term_object
            if not property_abs_test:
                term_object = Terminal(value=object_["object"][prop], unit="number")
                session.add(term_object)
                session.commit()

                abs_object = None
                inst_object = None
                print("Terminal object id", term_object.id)

            # If property is of RDFClass type then object is of abs_object type
            elif session.query(exists().where(RDFClass.name == keymap[object_["object"][prop]])).scalar():
                term_object = None
                abs_object = session.query(RDFClass).filter(RDFClass.name == keymap[object_["object"][prop]]).one()
                inst_object = None
                print("Abstract object id", abs_object.id)
            # Else object is of inst_object type
            else:
                term_object = None
                abs_object = None
                inst_object = session.query(Instance).filter(Instance.name == keymap[object_["object"][prop]]).one()
                print("Instance property id", inst_object.id)

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


def delete(id):
    """Delete an object and all its relations from DB given Instance id."""
    graph_data = session.query(Graph).filter(Graph.instance == id)
    instance_id = graph_data.all()[0].instance

    try:
        graph_data.delete()
        session.commit()
    except Exception as e:
        print(e)
        print("Something went wrong deleting Graph data!")

    try:
        for data in graph_data.all():
            # Can't delete values that are instances or abstract as they are common to various records
            if data.inst_predicate is not None and data.abs_predicate is None:
                try:
                    session.query(Terminal).filter(Terminal.id == data.term_object).delete()
                    session.commit()
                except Exception as e:
                    print(e)
                    print("Something went wrong deleting terminal objects!")

        # print(instance_id)
        try:
            session.query(Instance).filter(Instance.id == instance_id).delete()
            session.commit()
        except Exception as e:
            print(e)
            print("Something went wrong deleting instance!")

        return {204: "Object with id %s successfully deleted!" % (id)}
    except Exception as e:
        print(e)
        print("Something went horribly wrong!!")


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
print(get(7))
