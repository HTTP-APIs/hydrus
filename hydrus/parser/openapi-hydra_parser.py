"""
Module to take in Open Api Specification and convert it to HYDRA Api Doc

"""
import yaml
import json

from hydrus.hydraspec.doc_writer import HydraDoc, HydraClass, HydraClassProp, HydraClassOp



def generateEntrypoint():
    """
    Generates Entrypoint , Base Collection and Base Resource for the documentation
    """
    api_doc.add_baseCollection()
    api_doc.add_baseResource()
    api_doc.gen_EntryPoint()


def check_if_collection(schema_block):
    """
    checks if the provided schema block represents a collection or not
    :param schema_block: child of response object where schema is defined for return variables
    :return: collection (string)
    """
    print(schema_block)
    try:
        type = schema_block["type"]
        print("type is "+type)
        if type == "array":
            collection = "true"
        else:
            # TODO here in type we will get object,string,integer etc
            collection = type
    except KeyError:
        collection = "false"
    return collection


def get_class_details(class_location, doc):
    """
    fetches details of class and adds the class to the dict along with the classDefinition untill this point
    :param class_location: location of class definition in the doc , we extract name from here
    :param doc: the whole doc
    :return:
    """
    class_name = class_location[2]
    # we simply check if the class has been defined or not
    if class_name not in definitionSet:
        try:
            desc = doc[class_location[1]][class_location[2]]["description"]
        except KeyError:
            desc = class_location[2]
        classDefinition = HydraClass(class_name, class_name, desc, endpoint=True)

        properties = doc[class_location[1]][class_location[2]]["properties"]
        for prop in properties:
            # todo parse one more level to check 'type' and define class if needed
            # check required from required list and add when true
            classDefinition.add_supported_prop(HydraClassProp("vocab:" + prop,
                                                              prop,
                                                              required=False,
                                                              read=True,
                                                              write=True))
        classAndClassDefinition[class_name] = classDefinition
        definitionSet.add(class_name)
    else:
        return


def check_for_ref(doc, block):
    """
    checks the location of schema object in the given method , can be parameter or responses block
    and takes the collection from check_if_collection and passes to parent function
    :param doc: whole OAS defined doc
    :param block: the method block from doc
    :return: class name and collection variable
    """
    print("we entered check for ref for ")
    for obj in block["responses"]:

        try:
            print("in the try for reponses in CFR")
            print(block["responses"][obj]["schema"])
            collection = check_if_collection(block["responses"][obj]["schema"])
            print("from cfr the collection is "+collection)
            try:
                class_location = block["responses"][obj]["schema"]["$ref"].split('/')
            except KeyError:
                class_location = block["responses"][obj]["schema"]["items"]["$ref"].split('/')
            print("from cfr the class_location is ")
            print(class_location)
            get_class_details(class_location, doc)
            print("and we are returning from responses back ")
            return class_location[2], collection
        except KeyError:
            print("we are in the except of responses from cfr")
            print(block["responses"][obj])
            pass

    for obj in block["parameters"]:
        try:
            print("we are in try for paramerters")
            class_location = obj["schema"]["$ref"].split('/')
            print("we got class_location as ")
            print(class_location)
            get_class_details(class_location, doc)
            print("and we are returning from parameters")
            return class_location[2], "false"
        except KeyError:
            print("we are in except for parameters")
            pass

    print("we are returning from cfr with null values for ")
    print(block)
    return "null", "none"


def get_ops(param, method, class_name):
    """
    parses the method block and adds the operation to the already defined class definition
    :param param: the path block
    :param method: the method name ["post,"put","get"]
    :param class_name: class name
    """
    print(param)
    op_method = method
    op_expects = ""
    op_returns = None
    op_status = [{"statusCode": 200, "description": "dummyClass updated"}]
    try:
        op_name = param[method]["summary"]
    except KeyError:
        op_name = class_name
    try:
        parameters = param[method]["parameters"]
        for parameter in parameters:
            print("param is ")
            print(parameter)
            op_expects = "vocab:" + parameter["schema"]["$ref"].split('/')[2]
    except KeyError:
        op_expects = None
    # todo responses from definition set and status to be parsed yet
    print(param[method])
    try:
        responses = param[method]["responses"]
        op_status = responses
    except KeyError:
        op_returns = None
    print(" we are going to add an operation with name " + op_name)
    classAndClassDefinition[class_name].add_supported_op(HydraClassOp(op_name,
                                                                      op_method.upper(),
                                                                      op_expects,
                                                                      op_returns,
                                                                      op_status))


def get_paths(doc):
    """
    parent function for parsing the doc
    :param doc: the oas spec doc 
    """
    paths = doc["paths"]
    for path in paths:
        print("from paths we got path "+path)
        if len(path.split('/')) == 2:
            print("the url was of length one , hence we here")
            for method in paths[path]:
                print("inside method "+ method+ "for path "+path)
                class_name, collection = check_for_ref(doc, paths[path][method])
                print("the class name we got was "+class_name+"and the collection was "+collection)
                if collection != "none" and class_name != "null":
                    print("the collection and class var were suitable hence we here ")
                    get_ops(paths[path], method,class_name)

                    possiblePath = path.split('/')[1]
                    possiblePath = possiblePath.replace(possiblePath[0], possiblePath[0].upper())
                    print("the path is "+possiblePath)

                    if possiblePath in definitionSet:
                        print("we have found the class we parsed to be defined already ")
                        if collection is "true":
                            print("collection is true for this class")
                            api_doc.add_supported_class(classAndClassDefinition[class_name], collection=True)
                        else:
                            print("collection is false for this class ")
                            api_doc.add_supported_class(classAndClassDefinition[class_name], collection=False)
    generateEntrypoint()


if __name__ == "__main__":
    with open("../samples/petstore_open_api.yaml", 'r') as stream:
        try:
            doc = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    classAndClassDefinition = dict()
    definitionSet = set()
    classAndCollection = dict()
    info = doc["info"]
    desc = info["description"]
    title = info["title"]
    baseURL = doc["host"]
    name = doc["basePath"]
    api_doc = HydraDoc(name, title, desc, name, baseURL)
    get_paths(doc)


    # getClasses(doc)

    hydra_doc = api_doc.generate()

    dump = json.dumps(hydra_doc, indent=4, sort_keys=True)
    hydra_doc = '''"""\nGenerated API Documentation for Server API using server_doc_gen.py."""\n\ndoc = %s''' % dump
    hydra_doc = hydra_doc + '\n'
    hydra_doc = hydra_doc.replace('true', '"true"')
    hydra_doc = hydra_doc.replace('false', '"false"')
    hydra_doc = hydra_doc.replace('null', '"null"')
    f = open("../samples/hydra_doc_sample.py", "w")
    f.write(hydra_doc)
    f.close()
