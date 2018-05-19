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

