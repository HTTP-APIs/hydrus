"""Test script to enter data from random objects into old models(Depreciated)."""
from hydrus.data.crud import insert
from hydrus.data.generator import gen_cots



# Random generated objects

def insert_data(objects):
    """ Insert a list of obejcts to the database."""

    insertion_ids = []
    for object_ in objects:
        try:
            id_ = insert(object_)
            insertion_ids.append(id_)
        except:
            print("Error occured, skipping object.")
    return insertion_ids
# # Temporary storge for the Graph
# triple_store = list()
#
# # print(objects)
# Session = sessionmaker(bind=engine)
# session = Session()
#
#
# for object_ in objects:
#     # Query and get Rdf class
#     rdf_class_name = classes_keymap[object_["object"]["category"]]
#     print("Rdf class name", rdf_class_name)
#     rdf_class = session.query(RDFClass).filter(RDFClass.name == rdf_class_name).one()
#
#     # Get/Create Instance object
#     try:
#         resource = session.query(Instance).filter(Instance.name == object_["name"]).one()
#     except:
#         resource = Instance(name=object_["name"], type_=rdf_class.id)
#         session.add(resource)
#         session.commit()
#     print("Resource id", resource.id)
#
#     # Get/Create properties (both abstract and instance type)
#     for prop in object_["object"]:
#         if prop != "category":
#             # test to set property type (if true abstract)
#             try:
#                 # Check if property value is existing class
#                 abs_test_1 = session.query(exists().where(RDFClass.name == classes_keymap[object_["object"][prop]])).scalar()
#                 # Check if property value is existing instance
#                 abs_test_2 = session.query(exists().where(Instance.name == classes_keymap[object_["object"][prop]])).scalar()
#             except:
#                 abs_test_1 = False
#                 abs_test_2 = False
#
#             # Abstract property test (if true abstract)
#             property_abs_test = abs_test_1 or abs_test_2
#             if not property_abs_test:
#                 abstract_property = None
#                 try:
#                     property_ = session.query(Property).filter(Property.name == prop).one()
#                 except:
#                     # pdb.set_trace()
#                     property_ = Property(name=prop)
#                     session.add(property_)
#                     session.commit()
#                     print("Property id", property_.id)
#             else:
#                 property_ = None
#                 try:
#                     abstract_property = session.query(AbstractProperty).filter(AbstractProperty.name == prop).one()
#                 except:
#                     # pdb.set_trace()
#                     abstract_property = AbstractProperty(name=prop)
#                     session.add(abstract_property)
#                     session.commit()
#                     print("Abstract property id", abstract_property.id)
#
#             # Handle objects insertion/retrieval
#             # If property is not abstract then object is of type term_object
#             if not property_abs_test:
#                 term_object = Terminal(value=object_["object"][prop], unit="number")
#                 session.add(term_object)
#                 session.commit()
#
#                 abs_object = None
#                 inst_object = None
#                 print("Terminal object id", term_object.id)
#
#             # If property is of RDFClass type then object is of abs_object type
#             elif session.query(exists().where(RDFClass.name == classes_keymap[object_["object"][prop]])).scalar():
#                     term_object = None
#                     abs_object = session.query(RDFClass).filter(RDFClass.name == classes_keymap[object_["object"][prop]]).one()
#                     inst_object = None
#                     print("Abstract object id", abs_object.id)
#                 # Else object is of inst_object type
#             else:
#                 term_object = None
#                 abs_object = None
#                 inst_object = session.query(Instance).filter(Instance.name == classes_keymap[object_["object"][prop]]).one()
#                 print("Instance property id", inst_object.id)
#
#             # Create a temporary storage for Our Graph
#             triple = Graph(
#                 class_=rdf_class.id,
#                 instance=resource.id,
#                 abs_predicate=abstract_property.id if abstract_property is not None else None,
#                 inst_predicate=property_.id if property_ is not None else None,
#                 term_object=term_object.id if term_object is not None else None,
#                 abs_object=abs_object.id if abs_object is not None else None,
#                 inst_object=inst_object.id if inst_object is not None else None
#             )
#
#             triple_store.append(triple)
#
# # print(triple_store)
#
# # Insert everything into database
# session.add_all(triple_store)
# session.commit()
if __name__ == "__main__":
    objects = gen_cots(10)
    print(objects)
    insertion_ids = insert_data(objects)
    print(insertion_ids)
    print("Data insertion done!")
