"""
Take data from the data files and implement HYDRA spec.
"""

import data
from server.commons import ROOT, SERVE, HYDRA_DOC


# print(objects[0])

# filter the objects array
# use 'lifter' library to filter arrays
# https://github.com/EliotBerriot/lifter

template = {
  "@context": {
     "hydraspec": "http://www.w3.org/ns/hydraspec/context.jsonld",
  },
  "@id": None,
  "hydraspec:apiDocumentation": None,
  "@type": "hydraspec:Collection",
  "hydraspec:totalItems": None,
  "hydraspec:member": []
}

def collect_astronomy_resources(uri):
    """
    Serve an HYDRA collection loaded from a local dictionary.
    """

    objects = getattr(data, uri)['defines']  # get the data got the URL or raise AttributeError 

    # SERVE.format(class_=o.get('@type')[o.get('@type').rfind('/')+1:]
    members = [
        dict([
               ("@id", "{id_}".format(id_=o.get('@id'))),
               ("@type", "{class_}".format(class_=o.get('@type'))),
               ("hash", "{hash_}".format(hash_=o.get('hash')))
        ]) for o in objects
    ]

    template['@id'], template['hydraspec:totalItems'], template['hydraspec:member'] = ROOT + '/' + uri, len(members), members
    template['hydraspec:apiDocumentation'] = HYDRA_DOC.format(endpoint_=uri)

    return template


def collect_subclass_of(class_):
    """
    Serve an HYDRA collection of classes that are subclasses of a class
    """
    pass


