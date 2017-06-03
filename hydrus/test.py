from spacecraft_jsonld import spacecraft_data
from subsystem_jsonld import subsystem_data


def filter_objects_spacecraft(vocab=spacecraft_data, key='@type', value='http://www.w3.org/2002/07/owl#ObjectProperty'):
    """ Return a filtered list of objects from spacecraft_jsonld data, value pair and data. """
    obj_list = []
    for obj in vocab['defines']:
        if key in obj.keys():
            if type(obj[key]) == list and value in obj[key]:
                obj_list.append(obj)
    return obj_list


def filter_objects_subsystem(vocab=subsystem_data, key='@type', value='http://www.w3.org/2002/07/owl#ObjectProperty'):
    """ Return a filtered list of objects from spacecraft_jsonld data, value pair and data. """
    obj_list = []

    for obj in vocab['defines']:
        if key in obj.keys():
            if type(obj[key]) == list:
                for prop in obj[key]:
                    if prop['@id'] == value:
                        obj_list.append(obj)
            elif type(obj[key]) == dict:
                if '@id' in obj[key].keys():
                    if obj[key]['@id'] == value:
                        obj_list.append(obj)
    return obj_list

# print filter_objects_subsystem(subsystem_data)


def get_all_properties(obj_list):
    """ Get rdf:labels from a given list of objects. """
    rdf_labels = []
    for obj in obj_list:
        if obj['rdf:label'] not in rdf_labels:
            rdf_labels.append(obj['rdf:label'])

    return rdf_labels

# # print(get_rdf_lables(filter_objects_subsystem(subsystem_data)))


def get_abstract_properties(vocab):
    """Filter abstract properties from subsystem and spacecraft jsonld data.
        We use classes to filter abstract properties. Abstract properties are
        those predicates where both subject and object are of type #owl:class.

        Now, most of the triples have a Class as subject. So, that is of no use
        but we can use those classes which are being uses as objects in triples
        using 'owl:hasValue' to filter the properties in which they are being used.
    """
    abstract_properties = []
    for obj in vocab['defines']:
        # Find properties in which classes are being used as objects
        if "rdfs:subClassOf" in obj.keys():
            for obj1 in obj["rdfs:subClassOf"]:

                if "owl:hasValue" in obj1.keys():
                    if obj1['owl:onProperty']['@id'].rsplit('/', 1)[-1] not in abstract_properties:
                        abstract_properties.append(obj1['owl:onProperty']['@id'].rsplit('/', 1)[-1])
        # If any property is inverse of something that means its both subject and objects are classes
        elif 'owl:inverseOf' in obj.keys():
            if obj['owl:inverseOf']['@id'].rsplit('/', 1)[-1] not in abstract_properties:
                abstract_properties.append(obj['owl:inverseOf']['@id'].rsplit('/', 1)[-1])


    return abstract_properties
# print(get_abstract_properties(spacecraft_data))
# print(get_abstract_properties(spacecraft_data))

def merge_two_lists(list1, list2):
    """ Merge two list contents removing duplicate elements"""
    final_list = list1
    final_list.extend(x for x in list2 if x not in final_list)

    return final_list



subsystem_properties = get_all_properties(filter_objects_subsystem())
spacecraft_properties = get_all_properties(filter_objects_spacecraft())

all_properties = merge_two_lists(subsystem_properties, spacecraft_properties)
# print(all_properties)

subsystem_abstract_properties = get_abstract_properties(subsystem_data)
spacecraft_abstract_properties = get_abstract_properties(spacecraft_data)

all_abstract_properties = merge_two_lists(spacecraft_abstract_properties, subsystem_abstract_properties)

print(all_abstract_properties)
#OUTPUT
#['isDeployedIn', 'hasSubSystem', 'isSubsystemOf', 'isComponentOf', 'hasWireOutWith', 'hasWireInWith',
# 'function', 'subSystemType']

# Get instance properties using disjoint of all_properties and all_abstract_properties
instance_properties = list(set(all_properties) - set(all_abstract_properties))

print(instance_properties)
#OUTPUT
# ['minWorkingTemperature', 'hasMaxAmpere', 'hasPower', 'hasMinAmpere', 'holdsSensor', 'maxWorkingTemperature',
# 'hasSpecificImpulse','hasMonetaryValue', 'isStandard', 'hasVolume', 'embedSensor', 'manufacturer',
# 'typeOfPropellant', 'hasMass']







#
#
# def gen_properties(labels, type_="instance"):
#     """ Generate properties based on a given list of labels and property type (abstract/instance)."""
#     properties = []
#     if type_ == 'abstract':
#         for label in labels:
#             abstract_properties.append(models.AbstractProperty(name=label))
#     elif type_ == 'instance':
#         for label in labels:
#             abstract_properties.append(models.Property(name=label))
#
#     return properties
#
#
#
