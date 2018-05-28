"""
Module to take in Open Api Specification and convert it to HYDRA Api Doc

"""
import yaml
import json

from hydrus.hydraspec.doc_writer import HydraDoc, HydraClass, HydraClassProp, HydraClassOp

with open("../samples/openapi_sample.yaml", 'r') as stream:
    try:
        doc = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)


definitionSet = set()
classAndClassDefinition = dict()
hydra_doc = ""


def getClasses():
    """
    Get Definitions from Open Api specification and convert to Classes and supported Props for Hydra Documentation
    """
    definitions = doc["definitions"]

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

    get_ops()


def generateEntrypoint():
    """
    Generates Entrypoint , Base Collection and Base Resource for the documentation
    """
    api_doc.add_baseCollection()
    api_doc.add_baseResource()
    api_doc.gen_EntryPoint()


def get_ops():
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
                                                                                    op_method,
                                                                                    "vocab:" + op_expects,
                                                                                    op_returns,
                                                                                    op_status))
                api_doc.add_supported_class(classAndClassDefinition[possiblePath], collection=False)
                print("found" + possiblePath)

        else:
            print("not found")

        generateEntrypoint()


if __name__ == "__main__":
    info = doc["info"]
    desc = info["description"]
    title = info["title"]
    baseURL = doc["host"]
    name = doc["basePath"]
    api_doc = HydraDoc(name, title, desc, name, baseURL)
    getClasses()
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
