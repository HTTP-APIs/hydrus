from hydrus.data.astronomy import astronomy


objects = astronomy["defines"]

# filter the objects array
# use 'lifter' library to filter arrays
# https://github.com/EliotBerriot/lifter

def collect_astronomy_resources():
    return [o["rdf:label"] for o in objects]