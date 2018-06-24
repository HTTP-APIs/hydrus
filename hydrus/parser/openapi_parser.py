"""
Module to take in Open Api Specification and convert it to HYDRA Api Doc

"""
import yaml
import json
from typing import Any, Dict, Match, Optional, Tuple, Union, List, Set
from hydrus.hydraspec.doc_writer import HydraDoc, HydraClass, HydraClassProp, HydraClassOp


def try_catch_replacement(block: Any, get_this: str, default: Any) -> str:
    """
    replacement for the try catch blocks. HELPER FUNCTION
    :param block:
    :param get_this:
    :param default:
    :return:
    """
    try:
        return block[get_this]
    except KeyError:
        return default


def get_class_name(class_location: List[str]) -> str:
    """

    :param class_location: list containing the class location
    :return: name of class
    """
    return class_location[len(class_location)-1]


def get_data_at_location(class_location: List[str], doc: Dict[str,Any]) -> Dict[str,Any]:
    """

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


def generateEntrypoint(api_doc: HydraDoc) -> None:
    """
    Generates Entrypoint , Base Collection and Base Resource for the documentation
    """
    api_doc.add_baseCollection()
    api_doc.add_baseResource()
    api_doc.gen_EntryPoint()


def check_if_collection(schema_block: Dict[str, Any]) -> str:
    """
    checks if the provided schema block represents a collection or not
    :param schema_block: child of response object where schema is defined for return variables
    :return: collection (string)
    """
    print(schema_block)
    try:
        type = schema_block["type"]
        print("type is " + type)
        if type == "array":
            collection = "true"
        else:
            # TODO here in type we will get object,string,integer etc
            collection = type
    except KeyError:
        collection = "false"
    return collection


def get_class_details(class_location: List[str], doc: Dict["str", Any], classAndClassDefinition: Dict["str",HydraClass],
                      definitionSet: Set["str"]) -> None:
    """
    fetches details of class and adds the class to the dict along with the classDefinition untill this point
    :param classAndClassDefinition:
    :param definitionSet:
    :param class_location: location of class definition in the doc , we extract name from here
    :param doc: the whole doc
    :return:
    """
    class_name = get_class_name(class_location)
    # we simply check if the class has been defined or not
    if class_name not in definitionSet:

        desc = get_data_at_location(class_location,doc)
        classDefinition = HydraClass
        try:
            classDefinition = HydraClass(class_name, class_name, desc["description"], endpoint=True)
        except KeyError:
            classDefinition = HydraClass(class_name, class_name, class_name, endpoint=True)


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
            classDefinition.add_supported_prop(HydraClassProp("vocab:" + prop,
                                                              prop,
                                                              required=flag,
                                                              read=True,
                                                              write=True))
        classAndClassDefinition[class_name] = classDefinition
        definitionSet.add(class_name)
    else:
        return


def check_for_ref(doc: Dict["str", Any], block: Dict[str, Any], classAndClassDefinition: Dict["str",HydraClass],
                  definitionSet: Set["str"]) -> Tuple[str, str]:
    """
    checks the location of schema object in the given method , can be parameter or responses block
    and takes the collection from check_if_collection and passes to parent function
    :param classAndClassDefinition:
    :param definitionSet:
    :param doc: whole OAS defined doc
    :param block: the method block from doc
    :return: class name and collection variable
    """
    for obj in block["responses"]:

        try:
            print(block["responses"][obj]["schema"])
            collection = check_if_collection(block["responses"][obj]["schema"])
            print("from cfr the collection is " + collection)
            try:
                class_location = block["responses"][obj]["schema"]["$ref"].split(
                    '/')
            except KeyError:
                class_location = block["responses"][obj]["schema"]["items"]["$ref"].split(
                    '/')
            get_class_details(class_location, doc,classAndClassDefinition,definitionSet)
            return class_location[2], collection
        except KeyError:
            print(block["responses"][obj])
            pass

    # when we would be able to take arrays as parameters we will use check_if_collection here as well c
    for obj in block["parameters"]:
        print(obj)
        try:
            print("we are in try for paramerters")
            class_location = obj["schema"]["$ref"].split('/')
            print(class_location)
            get_class_details(class_location, doc, classAndClassDefinition , definitionSet)
            return class_location[2], "false"
        except KeyError:
            pass

    print(block)
    return "null", "none"


def get_ops(param: Dict["str", Any], method: str, class_name: str, classAndClassDefinition:Dict["str",HydraClass]) \
        -> None:
    """
    parses the method block and adds the operation to the already defined class definition
    :param classAndClassDefinition:
    :param param: the path block
    :param method: the method name ["post,"put","get"]
    :param class_name: class name
    """
    op_method = method
    op_expects = ""
    op_name = try_catch_replacement(param[method], "summary", class_name)
    op_status = list()
    try:
        parameters = param[method]["parameters"]
        for parameter in parameters:
            try:
                op_expects = "vocab:" + \
                    parameter["schema"]["$ref"].split('/')[2]
            except KeyError:
                op_expects = parameter["schema"]["type"]
    except KeyError:
        op_expects = None
    try:
        responses = param[method]["responses"]
        op_returns = ""
        for response in responses:
            if response != 'default':
                op_status.append({"statusCode": int(
                    response), "description": responses[response]["description"]})
            try:
                op_returns = "vocab:" + \
                    responses[response]["schema"]["$ref"].split('/')[2]
            except KeyError:
                pass
            if op_returns == "":
                try:
                    op_returns = "vocab:" + \
                        responses[response]["schema"]["items"]["$ref"].split(
                            '/')[2]
                except KeyError:
                    op_returns = try_catch_replacement(
                        responses[response]["schema"], "type", None)
    except KeyError:
        op_returns = None
    if len(op_status) == 0:
        op_status.append(
            {"statusCode": 200, "description": "Successful Operation"})

    print(" we are going to add an operation with name " + op_name)

    classAndClassDefinition[class_name].add_supported_op(HydraClassOp(op_name,
                                                                      op_method.upper(),
                                                                      op_expects,
                                                                      op_returns,
                                                                      op_status))


def get_paths(doc: Dict["str", Any], classAndClassDefinition: Dict["str",HydraClass], definitionSet: Set["str"],
              api_doc: HydraDoc) -> None:
    """
    parent function for parsing the doc
    :param api_doc: HydraDoc defined for the spec
    :param definitionSet: set containing all the classes already parsed
    :param classAndClassDefinition: dict containing class and respective defined class definition
    :param doc: the oas spec doc
    """
    paths = doc["paths"]
    for path in paths:
        if len(path.split('/')) == 2:
            for method in paths[path]:
                print("inside method " + method + "for path " + path)
                class_name, collection = check_for_ref(doc, paths[path][method], classAndClassDefinition, definitionSet)
                print("the class name we got was " + class_name + "and the collection was " + collection)

                if collection != "none" and class_name != "null":
                    get_ops(paths[path], method, class_name,classAndClassDefinition)
                    possiblePath = path.split('/')[1]
                    possiblePath = possiblePath.replace(
                        possiblePath[0], possiblePath[0].upper())
                    print("the path is " + possiblePath)

                    if possiblePath in definitionSet:
                        if collection is "true":
                            api_doc.add_supported_class(
                                classAndClassDefinition[class_name], collection=True)
                        else:
                            api_doc.add_supported_class(classAndClassDefinition[class_name], collection=False)
    generateEntrypoint(api_doc)


def parse(doc: Dict[str,Any]) -> str:
    """
    parent function for parsing the doc
    :param doc: the open api documentation
    :return:  hydra doc created
    """
    classAndClassDefinition = dict()  # type: Dict[str,HydraClass]
    definitionSet = set()  # type: Set[str]
    info = try_catch_replacement(doc, "info", "")

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
    get_paths(doc, classAndClassDefinition, definitionSet, api_doc)
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
