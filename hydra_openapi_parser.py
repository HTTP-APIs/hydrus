from hydrus.hydraspec.doc_maker import create_doc
from hydrus.hydraspec.doc_writer_sample_output import doc

import yaml
from hydrus.data.doc_parse import get_classes, get_all_properties

# below stuff is temporary
apidoc = create_doc(doc, "http://localhost:8080/", "api")
apiSpec = apidoc.generate()

dataDump = dict(
    {
        "swagger": '2.0',
        "info": {
            "title": apiSpec["title"],
            "description": apiSpec["description"]
        },
        "host": "hydrus.com",
        "schemes": ("https", "http"),
        "basePath ": "/",
        "paths": {

        },
        "definitions": {

        }
    }
)

# classes = get_classes(apiSpec)
# titles = set()
"""these functions will be in another helper module """


# this function is to be used to replace multiple ifs with switch case/dict later
def populate_data():
    pass


def add_definitions(classes):
    for item in classes:
        title = ""
        description = ""
        for anItem in item:
            # try using populate_data here

            if anItem == "title":
                title = item[anItem]
            elif anItem == "description":
                description = item[anItem]
            elif anItem == "supportedProperty":
                for properties in item[anItem]:
                    print(properties['title'])


            # make varibles here assign in dict at end , push to dataDump
            if title and description:
                definition = dict(
                    {
                        title: {
                            "type": "object",
                            "description": description
                        }
                    }
                )
                dataDump["definitions"].update(definition)
                title = ""
                description = ""
                # add title and props to dict


def start_parsing(apiSpec):
    """this function is to start parsing , classes ->definitions , props -> definition.schema , ops -> paths . We shall try
    that all this get possible in as less for loops as possible.
    """
    add_definitions(get_classes(apiSpec))


start_parsing(apiSpec)


with open('result.yml', 'w') as yaml_file:
    yaml.safe_dump(dataDump, yaml_file, default_flow_style=False)