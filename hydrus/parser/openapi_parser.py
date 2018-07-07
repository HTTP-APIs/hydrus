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


def generate_empty_object() -> Dict[str, Any]:
    """
    Generate Empty object
    :return: empty object
    """
    object = {
        "class_name": "",
        "class_definition": HydraClass,
        "prop_definition": list(),
        "op_definition": list(),
        "collection": False,
        "path": ""
    }
    return object


def check_collection(class_name: str,
                     global_: Dict[str,
                                   Any],
                     schema_obj: Dict[str, Any],
                     method: str)->Dict[str,
                                        Any]:
    """
    Checks if the method is collection or not , checks if the method is valid
    :param class_name: name of class being parsed
    :param global_: global state
    :param schema_obj: the dict containing the method object
    :param method: method ie GET,POST,PUT,DELETE
    :return: object that is formed or updated
    """
    collection = bool
    # get the object type from schema block
    try:
        type = schema_obj["type"]
        # if object type is array it means the method is a collection
        if type == "array":
            collection = True
        else:
            # here type should be "object"
            collection = False
    except KeyError:
        collection = False
    # checks if the method is something like 'pet/{petid}'
    if valid_endpoint(method) == "collection" and collection == False:
        collection = True
    object_ = generate_empty_object()
    # checks if the method is supported by parser at the moment or not
    # TODO see if it is required
    flag = check_array_param(global_["doc"]["paths"][method])

    if valid_endpoint(method) != "False":
        try:
            # if the class has already been parsed we will update the
            # collection var
            if not global_[class_name]["collection"]:
                global_[class_name]["collection"] = True
        except KeyError:
            # if the class has not been parsed we will insert the object
            object_["class_name"] = class_name
            object_["collection"] = collection
            global_[class_name] = object_
    return object_


def check_array_param(paths_: Dict[str, Any]) -> bool:
    """
    Check if the path is supported or not
    :param paths_: the path object from doc
    :return: TRUE if the path is supported
    """
    for method in paths_:
        for param in paths_[method]["parameters"]:
            try:
                if param["type"] == "array" and method == "get":
                    return False
            except KeyError:
                pass
    return True


def valid_endpoint(path: str) -> str:
    """
    Checks is the path ie endpoint is constructed properly or not
    rejects 'A/{id}/B/C'
    :param path: endpoint
    :return:
    """
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


def sanitise_path(path: str)->str:
    """
    Removed any variable present in the path
    :param path:
    :return:
    """
    path_ = path.split('/')
    new_path = list()
    for subPath in path_:
        if "{" in subPath:
            pass
        else:
            new_path.append(subPath)

    return '/'.join(new_path)


def get_class_details(global_: Dict[str,
                                    Any],
                      data: Dict[str,
                                 Any],
                      class_name: str,
                      path="") -> None:
    """
    fetches details of class and adds the class to the dict along with the classDefinition until this point
    :param global_: global state
    :param class_name: name of class
    :param data: data from the location given in $ref
    :param path: Optional , custom enpoint to be assigned
    :return: None
    """
    doc = global_["doc"]
    path = sanitise_path(path)

    class_name = class_name
    # we simply check if the class has been defined or not
    if class_name not in global_["class_names"]:

        desc = data
        try:
            classDefinition = HydraClass(
                class_name,
                class_name,
                desc["description"],
                endpoint=True,
                path=path)
        except KeyError:
            classDefinition = HydraClass(
                class_name, class_name, class_name, endpoint=True, path=path)

        properties = data["properties"]
        try:
            required = data["required"]
        except KeyError:
            required = set()
        for prop in properties:
            # todo parse one more level to check 'type' and define class if needed
            # check required from required list and add when true
            flag = False
            if prop in required and len(required) > 0:
                flag = True
            # TODO copy stuff from semantic ref branch regarding prop exists in
            # definitionset or not
            global_[class_name]["prop_definition"].append(HydraClassProp(
                "vocab:" + prop, prop, required=flag, read=True, write=True))
        global_[class_name]["path"] = path
        global_[class_name]["class_definition"] = classDefinition
        global_["class_names"].add(class_name)


def check_for_ref(global_: Dict[str, Any],
                  path: str,
                  block: Dict[str,Any])->str:
    """
    Checks for references in responses and parameters key , and adds classes to state
    :param global_: global state
    :param path: endpoint
    :param block: block containing specific part of doc
    :return: class name
    """
    # will check if there is an external ref , go to that location , add the class in globals , will also verify
    # if we can parse this method or not , if all good will return class name
    for obj in block["responses"]:
        try:
            try:
                class_location = block["responses"][obj]["schema"]["$ref"].split(
                    '/')
            except KeyError:
                class_location = block["responses"][obj]["schema"]["items"]["$ref"].split(
                    '/')
            object_ = check_collection(
                class_name=class_location[2],
                global_=global_,
                schema_obj=block["responses"][obj]["schema"],
                method=path)

            if object_["class_name"] == "":
                # cannot parse because method not supported
                return object_["class_name"]
            get_class_details(
                global_,
                get_data_at_location(
                    class_location,
                    global_["doc"]),
                get_class_name(class_location),
                path=path)
            return class_location[2]
        except KeyError:
            pass

    # when we would be able to take arrays as parameters we will use
    # check_if_collection here as well c
    for obj in block["parameters"]:
        try:
            try:
                class_location = obj["schema"]["$ref"].split('/')
            except KeyError:
                class_location = obj["schema"]["items"]["$ref"].split('/')
            object_ = check_collection(
                class_location[2], global_, obj["schema"], path)
            if object_["class_name"] == "":
                # cannot parse because method not supported
                return object_["class_name"]
            get_class_details(
                global_,
                get_data_at_location(
                    class_location,
                    global_["doc"]),
                get_class_name(class_location),
                path=path)
            return class_location[2]
        except KeyError:
            pass
    # cannot parse because no external ref
    return ""


def allow_parameter(parameter: Dict[str, Any])->bool:
    """
    Checks the validity of params that are to be processed
    according to  rules of param passing
    :param parameter: the parameter to be parsed
    :return: if its valid or not
    """
    # can add rules about param processing
    # param can be in path too , that is already handled when we declared
    # the class as collection from the endpoint
    params_location = ["body"]
    if parameter["in"] not in params_location:
        return False
    return True


def type_ref_mapping(type: str)->str:
    """
    Returns semantic ref for OAS data types
    :param type: data type
    :return: ref
    """
    dataType_ref_map = dict()
    # todo add support for byte , binary , password ,double data types
    dataType_ref_map["integer"] = "https://schema.org/Integer"
    dataType_ref_map["string"] = "https://schema.org/Text"
    dataType_ref_map["long"] = "http://books.xmlschemata.org/relaxng/ch19-77199.html"
    dataType_ref_map["float"] = "https://schema.org/Float"
    dataType_ref_map["boolean"] = "https://schema.org/Boolean"
    dataType_ref_map["dateTime"] = "https://schema.org/DateTime"
    dataType_ref_map["date"] = "https://schema.org/Date"
    return dataType_ref_map[type]


def get_parameters(global_: Dict[str, Any],
                   path: str, method: str, class_name: str)->str:
    """
    Parse paramters from method object
    :param global_: global state
    :param path: endpoint
    :param method: method under consideration
    :param class_name: name of class
    :return: param
    """
    param = str
    for parameter in global_["doc"]["paths"][path][method]["parameters"]:
        if allow_parameter(parameter):
            try:
                # check if class has been parsed
                if parameter["schema"]["$ref"].split(
                        '/')[2] in global_["class_names"]:
                    param = "vocab:" + \
                        parameter["schema"]["$ref"].split('/')[2]

                else:
                    # if not go to that location and parse and add
                    get_class_details(
                        global_,
                        get_data_at_location(
                            parameter["schema"]["$ref"]),
                        parameter["schema"]["$ref"].split('/')[2],
                        path=path)
                    param = "vocab:" + \
                            parameter["schema"]["$ref"].split('/')[2]
            except KeyError:
                type = parameter["type"]
                if type == "array":
                    # TODO change this after we find a way to represent array
                    # in parameter using semantics
                    items = parameter["schema"]["items"]
                    try:
                        if items["$ref"].split(
                                '/')[2] in global_["class_names"]:
                            param = "vocab" + items["$ref"].split('/')[2]
                        else:
                            get_class_details(
                                global_, get_data_at_location(
                                    items["$ref"]), items["$ref"].split('/')[2], path=path)
                            param = "vocab" + items["$ref"].split('/')[2]
                    except KeyError:
                        param = type_ref_mapping(items["type"])
                elif type == "object":
                    param = "string"
                else:
                    param = type_ref_mapping(type)

    return param


def get_ops(global_: Dict[str, Any], path: str,
            method: Dict[str, Any], class_name: str)->None:
    """
    Get operations from path object and store in global path
    :param global_: global state
    :param path: endpoint
    :param method: method block
    :param class_name:class name
    """
    op_method = method
    op_expects = None
    op_name = try_catch_replacement(
        global_["doc"]["paths"][path][method],
        "summary",
        class_name)
    op_status = list()
    op_expects = get_parameters(global_, path, method, class_name)
    try:
        responses = global_["doc"]["paths"][path][method]["responses"]
        op_returns = None
        for response in responses:
            if response != 'default':
                op_status.append({"statusCode": int(
                    response), "description": responses[response]["description"]})
            try:
                op_returns = "vocab:" + \
                    responses[response]["schema"]["$ref"].split('/')[2]
            except KeyError:
                pass
            if op_returns is None:
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

    global_[class_name]["op_definition"].append(HydraClassOp(
        op_name, op_method.upper(), op_expects, op_returns, op_status))


def get_paths(global_: Dict[str, Any]) -> None:
    """
    Parse paths iteratively
    :param global_: Global state
    """
    paths = global_["doc"]["paths"]
    for path in paths:
        for method in paths[path]:
            class_name = check_for_ref(global_, path, paths[path][method])
            if class_name != "":
                # do further processing
                get_ops(global_, path, method, class_name)


def parse(doc: Dict[str, Any]) -> str:
    """
    To parse the "info" block and create Hydra Doc
    :param doc: the open api documentation
    :return:  hydra doc created
    """
    classAndClassDefinition = dict()  # type: Dict[str,HydraClass]
    definitionSet = set()  # type: Set[str]
    info = try_catch_replacement(doc, "info", "")
    global_ = dict()
    global_["class_names"] = definitionSet
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
    for name in global_["class_names"]:
        for prop in global_[name]["prop_definition"]:
            global_[name]["class_definition"].add_supported_prop(prop)
        for op in global_[name]["op_definition"]:
            global_[name]["class_definition"].add_supported_op(op)
        api_doc.add_supported_class(
            global_[name]["class_definition"],
            global_[name]["collection"],
            collection_path=global_[name]["path"])

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
