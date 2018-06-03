"""
Module to take in Open Api Specification and convert it to HYDRA Api Doc

"""
import yaml
import json

from hydrus.hydraspec.doc_writer import HydraDoc, HydraClass, HydraClassProp, HydraClassOp

hydra_doc = ""


def getClasses(doc):
    """
    Get Definitions from Open Api specification and convert to Classes and supported Props for Hydra Documentation
    """
    definitions = doc["definitions"]
    definitionSet = set()
    classAndClassDefinition = dict()
    for class_ in definitions:
        try:
            desc = definitions[class_]["description"]
        except KeyError:
            desc = class_
        classDefinition = HydraClass(class_, class_, desc, endpoint=False)
        properties = definitions[class_]["properties"]
        classAndClassDefinition[class_] = classDefinition
        definitionSet.add(class_)
        api_doc.add_supported_class(classDefinition, collection=False)
        for prop in properties:
            new_prop = HydraClassProp("vocab:" + prop, prop, required=False, read=True, write=True)
            classAndClassDefinition[class_].add_supported_prop(new_prop)

    get_ops(doc, definitionSet, classAndClassDefinition)


def generateEntrypoint():
    """
    Generates Entrypoint , Base Collection and Base Resource for the documentation
    """
    api_doc.add_baseCollection()
    api_doc.add_baseResource()
    api_doc.gen_EntryPoint()


def get_ops(doc, definitionSet, classAndClassDefinition):
    """
    Parses Paths from the Open Api Spec and creates supported operations for the paths which we have defined classes for
    we check if the path has a class defined , if it does we parse the methods and add the information parsed to Hydra

    :return:
    """
    paths = doc["paths"]

    for path in paths:
        possiblePath = path.split('/')[1]
        # dirty hack , do  case insensitive search more gracefully
        possiblePath = possiblePath.replace(possiblePath[0], possiblePath[0].upper())
        # check if the path name exists in the classes defined
        if possiblePath in definitionSet and len(path.split('/')) == 2:
            for method in paths[path]:
                op_method = method
                op_expects = ""
                op_returns = None
                op_status = [{"statusCode": 200, "description": "dummyClass updated"}]
                try:
                    op_name = paths[path][method]["summary"]
                except KeyError:
                    op_name = possiblePath
                try:
                    parameters = paths[path][method]["parameters"]
                    for param in parameters:
                        op_expects = param["schema"]["$ref"].split('/')[2]
                except KeyError:
                    op_expects = None
                try:
                    responses = paths[path][method]["responses"]
                    op_status = responses
                except KeyError:
                    op_returns = None
                classAndClassDefinition[possiblePath].add_supported_op(HydraClassOp(op_name,
                                                                                    op_method.upper(),
                                                                                    "vocab:" + op_expects,
                                                                                    op_returns,
                                                                                    op_status))
                api_doc.add_supported_class(classAndClassDefinition[possiblePath], collection=False)
                print("found" + possiblePath)

        else:
            print("not found")

        generateEntrypoint()


def add_class(doc , block , class_name , collection ):
    # make a var to store class name and collection  bool
    pass


def check_if_collection(schema_block):
    print("hehehhee")
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
            classDefinition.add_supported_prop(HydraClassProp("vocab:" + prop, prop, required=False, read=True, write=True))
        classAndClassDefinition[class_name] = classDefinition
        definitionSet.add(class_name)
    else:
        return


def check_for_ref(doc, block):
    for obj in block["responses"]:
        collection = "none"
        class_location = list(["null", "null", "null"])
        try:
            collection = check_if_collection(block["responses"][obj]["schema"])
            print("collection from for is "+collection)
            class_location = block["responses"][obj]["schema"]["$ref"].split('/')
            get_class_details(class_location, doc)
            return class_location[2], collection
        except KeyError:
            return class_location[2], collection

    for obj in block["parameters"]:
        class_location = list(["null", "null", "null"])
        try:
            class_location = obj["schema"]["$ref"].split('/')
            get_class_details(class_location, doc)
            print("in try")
            return class_location[2], "false"
        except KeyError:
            print("in except")
            return class_location[2], "false"

    print("we are here let")



def get_paths(doc):
    paths = doc["paths"]
    for path in paths:
        if len(path.split('/')) == 2:
            for method in paths[path]:
                class_name, collection = check_for_ref(doc, paths[path][method])
                if collection != "none" and class_name != "null":
                    op_method = method
                    op_expects = ""
                    op_returns = None
                    op_status = [{"statusCode": 200, "description": "dummyClass updated"}]
                    try:
                        op_name = paths[path][method]["summary"]
                    except KeyError:
                        op_name = class_name
                    # expects to be found from the definition set
                    try:
                        parameters = paths[path][method]["parameters"]
                        for param in parameters:
                            op_expects = param["schema"]["$ref"].split('/')[2]
                    except KeyError:
                        op_expects = None
                    # todo responses from definition set and status to be parsed yet
                    try:
                        responses = paths[path][method]["responses"]
                        op_status = responses
                    except KeyError:
                        op_returns = None
                    classAndClassDefinition[class_name].add_supported_op(HydraClassOp(op_name,
                                                                                      op_method.upper(),
                                                                                      "vocab:" + op_expects,
                                                                                      op_returns,
                                                                                      op_status))
                    possiblePath= path.split('/')[1]
                    possiblePath = possiblePath.replace(possiblePath[0], possiblePath[0].upper())

                    if possiblePath in definitionSet:
                        pass
                    if collection is "true":
                        print("hit")
                        api_doc.add_supported_class(classAndClassDefinition[class_name], collection=True)
                    else:
                        print("miss")
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
