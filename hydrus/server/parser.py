from data.astronomy import astronomy
from server.commons import ROOT, SERVE, HYDRA_DOC


objects = astronomy['defines']

# print(objects[0])

# filter the objects array
# use 'lifter' library to filter arrays
# https://github.com/EliotBerriot/lifter

template = {
  "@context": {
     "hydra": "http://www.w3.org/ns/hydra/context.jsonld",
  },
  "@id": None,
  "hydra:apiDocumentation": None,
  "@type": "hydra:Collection",
  "hydra:totalItems": None,
  "hydra:member": []
}

def collect_astronomy_resources(uri):
    """
    Serve an HYDRA collection loaded from a local dictionary.
    """

    # SERVE.format(class_=o.get('@type')[o.get('@type').rfind('/')+1:]
    members = [
        dict([
               ("@id", "{id_}".format(id_=o.get('@id'))),
               ("@type", "{class_}".format(class_=o.get('@type'))),
               ("hash", "{hash_}".format(hash_=o.get('hash')))
        ]) for o in objects
    ]

    template['@id'], template['hydra:totalItems'], template['hydra:member'] = ROOT + '/' + uri, len(members), members
    template['hydra:apiDocumnetation'] = HYDRA_DOC.format(uri)

    return template


def collect_subclass_of(class_):
    """
    Serve an HYDRA collection of classes that are subclasses of a class
    """
    pass


