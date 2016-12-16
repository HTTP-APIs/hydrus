from data.astronomy import astronomy

ROOT = '/api'
SERVE = '/api/{class_}/{label_}'
HYDRA_DOC = "/api/hydra/{}"


import hashlib
m = hashlib.md5()

# add an hashed id to the resources
for i, a in enumerate(astronomy['defines']):
    m.update(
        bytes(a.get('rdf:label', ValueError()), 'utf-8')
    )
    astronomy['defines'][i]['hash'] = m.hexdigest()
