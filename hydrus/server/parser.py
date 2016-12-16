from data.astronomy import astronomy
from server.commons import ROOT, SERVE


objects = astronomy['defines']

# print(objects[0])

# filter the objects array
# use 'lifter' library to filter arrays
# https://github.com/EliotBerriot/lifter

template = {
  "@context": "http://www.w3.org/ns/hydra/context.jsonld",
  "@id": None,
  "@type": "Collection",
  "totalItems": None,
  "member": []
}

def collect_astronomy_resources(uri):

    # SERVE.format(class_=o.get('@type')[o.get('@type').rfind('/')+1:]
    members = [
        dict([
               ("@id", "{id_}".format(id_=o.get('@id'))),
               ("@type", "{class_}".format(class_=o.get('@type')))
        ]) for o in objects
    ]

    template['@id'], template['totalItems'], template['member'] = uri, len(members), members

    return template


