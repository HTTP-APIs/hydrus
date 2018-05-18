import yaml

with open("openapi_sample.yaml", 'r') as stream:
    try:
        doc = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

