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


def check_collection(class_name, global_,schema_obj):
    try:
        type = schema_obj["type"]
        print("type is " + type)
        if type == "array":
            collection = True
        else:
            collection = False
    except KeyError:
        collection = False

    

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
            check_collection(class_name=class_location[2],global_=global_,schema_obj=block["responses"][obj]["schema"])
            get_class_details(
                class_location,
                doc,
                classAndClassDefinition,
                definitionSet)
            return class_location[2], collection
        except KeyError:
            print("external ref not found in responses ")
            print(block["responses"][obj])
            pass

    # when we would be able to take arrays as parameters we will use
    # check_if_collection here as well c
    for obj in block["parameters"]:
        print(obj)
        try:
            print("we are in try for paramerters")
            class_location = obj["schema"]["$ref"].split('/')
            print(class_location)
            get_class_details(
                class_location,
                doc,
                classAndClassDefinition,
                definitionSet)
            return class_location[2], False
        except KeyError:
            pass

    print(block)
    return "null", "none"

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
