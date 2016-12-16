from data.astronomy import astronomy


objects = astronomy['defines']

print(objects[0])

# filter the objects array
# use 'lifter' library to filter arrays
# https://github.com/EliotBerriot/lifter

def collect_astronomy_resources():
    return [o.get('rdf:label', KeyError()) for o in objects]