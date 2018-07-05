"""
Module to take in Open Api Specification and convert it to HYDRA Api Doc

"""
import yaml
import json
from typing import Any, Dict, Match, Optional, Tuple, Union, List, Set
from hydrus.hydraspec.doc_writer import HydraDoc, HydraClass, HydraClassProp, HydraClassOp


def try_catch_replacement(block: Any, get_this: str, default: Any) -> str:
    """
    Replacement for the try catch blocks. HELPER FUNCTION
    :param block: Data from where information has to be parsed
    :param get_this: The key using which we have to fetch values from the block
    :param default: default value incase the key does not exist
    :return: string containing the value
    """
    try:
        return block[get_this]
    except KeyError:
        return default

def generateEntrypoint(api_doc: HydraDoc) -> None:
    """
    Generates Entrypoint , Base Collection and Base Resource for the documentation
    :param api_doc: contains the Hydra Doc created
    """
    api_doc.add_baseCollection()
    api_doc.add_baseResource()
    api_doc.gen_EntryPoint()

def generate_empty_object():
    object = {
        "class_name":"",
        "class_definition":HydraClass(),
        "prop_definition":list(),
        "op_definition":list(),
        "collection": False
    }
    return object



def check_collection(class_name, global_,schema_obj,method):
    collection = bool
    # get the object type from schema block
    try:
        type = schema_obj["type"]
        print("type is " + type)
        # if object type is array it means the method is a collection
        if type == "array":
            collection = True
        else:
            # here type should be "object"
            collection = False
    except KeyError:
        collection = False

    # checks if the method is something like 'pet/{petid}'
    if valid_endpoint(method)=="collection" and collection==False:
        collection=True

    object_ = generate_empty_object()
    # checks if the method is supported by parser at the moment or not
    if check_array_param(global_["doc"]["paths"][method]) and valid_endpoint(method)!="False" :
        try :
            # if the class has already been parsed we will update the collection var
            name = global_[class_name]
            if not global_[class_name]["collection"]:
                global_[class_name]["collection"]=True
        except KeyError:
            # if the class has not been parsed we will insert the object
            object_["class_name"] = class_name
            object_["collection"]=collection
            global_[class_name]= object_

    return object_


def check_array_param(paths_):
    for method in paths_:
        if paths_[method]["parameters"]["type"] == "array" and method == "get":
            return False
    return True

def valid_endpoint(path):
    # "collection" or true means valid
    path_ = path.split('/')
    for subPath in path_:
        if "{" in subPath:
            if subPath != path_[len(path_) - 1]:
                return "False"
            else:
                return "Collection"
    return "True"

def get_class_name(class_location: List[str]) -> str:
    """
    To get class name from the class location reference given
    :param class_location: list containing the class location
    :return: name of class
    """
    return class_location[len(class_location) - 1]

def get_data_at_location(
        class_location: List[str], doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    TO get the dict at the class location provided
    :param class_location: list containing the class location
    :param doc: the open api doc
    :return: class defined at class location in the doc
    """
    data = doc
    index = 0
    while index <= len(class_location) - 3:
        data = data[class_location[index + 1]][class_location[index + 2]]
        index = index + 1
    return data

def get_class_details(class_location: List[str],global_) -> None:
    """
    fetches details of class and adds the class to the dict along with the classDefinition until this point
    :param classAndClassDefinition:  dict containing class and respective defined class definition
    :param definitionSet: set containing the names of all parsed classes
    :param class_location: location of class definition in the doc , we extract name from here
    :param doc: the whole doc
    :return: None
    """
    doc = global_["doc"]
    class_name = get_class_name(class_location)
    # we simply check if the class has been defined or not
    if class_name not in global_["class_names"]:

        desc = get_data_at_location(class_location, doc)
        try:
            classDefinition = HydraClass(
                class_name, class_name, desc["description"], endpoint=True)
        except KeyError:
            classDefinition = HydraClass(
                class_name, class_name, class_name, endpoint=True)

        properties = get_data_at_location(class_location, doc)["properties"]
        try:
            required = get_data_at_location(class_location, doc)["required"]
        except KeyError:
            required = set()
        for prop in properties:
            # todo parse one more level to check 'type' and define class if needed
            # check required from required list and add when true
            flag = False
            if prop in required and len(required) > 0:
                flag = True
            # TODO copy stuff from semantic ref branch regarding prop exists in definitionset or not
            global_[class_name]["prop_definition"].append(HydraClassProp("vocab:" + prop,
                                                              prop,
                                                              required=flag,
                                                              read=True,
                                                              write=True))

        global_[class_name]["class_definition"] = classDefinition
        global_["class_names"].add(class_name)





def check_for_ref(global_, method):
    # will check if there is an external ref , go to that location , add the class in globals , will also verify
    # if we can parse this method or not , if all good will return class name
    block = global_["doc"]["paths"][method]
    for obj in block["responses"]:
        try:
            try:
                class_location = block["responses"][obj]["schema"]["$ref"].split(
                    '/')
            except KeyError:
                class_location = block["responses"][obj]["schema"]["items"]["$ref"].split(
                    '/')
            object_=check_collection(class_name=class_location[2],global_=global_,schema_obj=block["responses"][obj]["schema"],
                             method=method)

            if object_["class_name"]=="":
                # cannot parse because method not supported
                return object_["class_name"]
            get_class_details(
                class_location,
                global_)
        except KeyError:
            print("external ref not found in responses ")
            pass

    # when we would be able to take arrays as parameters we will use
    # check_if_collection here as well c
    for obj in block["parameters"]:
        try:
            class_location = obj["schema"]["$ref"].split('/')
            print(class_location)
            get_class_details(
                class_location,
                global_)
            return class_location[2]
        except KeyError:
            pass
    # cannot parse because no external ref
    return ""

def get_paths(global_) -> None:
    doc = global_["doc"]
    for method in doc["paths"]:
        class_name = check_for_ref(global_,method)
        if class_name != "":
            pass



def parse(doc: Dict[str, Any]) -> str:
    """
    To parse the "info" block and create Hydra Doc
    :param doc: the open api documentation
    :return:  hydra doc created
    """
    classAndClassDefinition = dict()  # type: Dict[str,HydraClass]
    definitionSet = set()  # type: Set[str]
    info = try_catch_replacement(doc, "info", "")
    global_= dict()
    global_["class_names"]=definitionSet
    global_["doc"] = doc

    if info != "":
        desc = try_catch_replacement(info, "description", "not defined")
        title = try_catch_replacement(info, "title", "not defined")
    else:
        desc = "not defined"
        title = "not defined"
    # todo throw error if desc or title dont exist

    baseURL = try_catch_replacement(doc, "host", "localhost")
    name = try_catch_replacement(doc, "basePath", "api")
    schemes = try_catch_replacement(doc, "schemes", "http")
    api_doc = HydraDoc(name, title, desc, name, schemes[0] + "://" + baseURL)
    get_paths(global_)
    generateEntrypoint(api_doc)
    hydra_doc = api_doc.generate()
    dump = json.dumps(hydra_doc, indent=4, sort_keys=True)
    hydra_doc = '''"""\nGenerated API Documentation for Server API using server_doc_gen.py."""\n\ndoc = %s''' % dump
    hydra_doc = hydra_doc + '\n'
    hydra_doc = hydra_doc.replace('true', '"true"')
    hydra_doc = hydra_doc.replace('false', '"false"')
    hydra_doc = hydra_doc.replace('null', '"null"')

    return hydra_doc


if __name__ == "__main__":
    with open("../samples/petstore_openapi.yaml", 'r') as stream:
        try:
            doc = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    documentation = parse(doc)

    f = open("../samples/hydra_doc_sample.py", "w")
    f.write(documentation)
    f.close()
