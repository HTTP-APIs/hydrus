import yaml
from doc_writer import HydraDoc, HydraClass, HydraClassProp, HydraClassOp

with open("openapi_sample.yaml", 'r') as stream:
    try:
        doc = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)
# api name , desciption , baseURl ,title
info=doc["info"]
desc = info["description"]
title = info["title"]
baseURL = doc["host"]
name = doc["basePath"]
api_doc = HydraDoc(name,title,desc,name,baseURL)
"""get title , desc, props ,ops"""
definitions = doc["definitions"]
for class_ in definitions:
    try:
        desc=definitions[class_]["description"]
    except KeyError:
        desc=class_
    classDefinition = HydraClass(class_,class_,desc,endpoint=False)
    properties = definitions[class_]["properties"]
    for prop in properties:
        new_prop = HydraClassProp("vocab:"+prop,prop, required=False, read=True, write=True)
        classDefinition.add_supported_prop(new_prop)
    api_doc.add_supported_class(classDefinition,collection=False)

api_doc.add_baseCollection()
api_doc.add_baseResource()
api_doc.gen_EntryPoint()
hydra_doc = api_doc.generate()
if __name__ == "__main__":
    import json
    dump = json.dumps(hydra_doc, indent=4, sort_keys=True)
    hydra_doc = '''"""\nGenerated API Documentation for Server API using server_doc_gen.py."""\n\ndoc = %s''' % dump
    hydra_doc = hydra_doc + '\n'
    hydra_doc = hydra_doc.replace('true', '"true"')
    hydra_doc = hydra_doc.replace('false', '"false"')
    hydra_doc = hydra_doc.replace('null', '"null"')
    f = open("hydra_doc_sample.py", "w")
    f.write(hydra_doc)
    f.close()
