global_doc = {
  "@context": {
     "hydra": "http://www.w3.org/ns/hydra/context.jsonld",
  },
  "@id": "/api",
  "@type": "hydra:ApiDocumentation",
  "hydra:title": "The name of the API",
  "hydra:description": "A short description of the API",
  "hydra:entrypoint": "/api",
  "hydra:supportedClass": [
    
  ],
  "hydra:possibleStatus": [
    
  ]
}

def make_doc(view):
  return {
    "@context": {
      "hydra": "http://www.w3.org/ns/hydra/context.jsonld"
    },
    "@id": "/api/hydra/{}".format(view),
    "@type": "hydra:ApiDocumentation",
    "hydra:title": "{}".format(view),
    "hydra:description": "",
    "hydra:entrypoint": "/api/{}".format(view),
    "hydra:supportedClass": [
      
    ],
    "hydra:possibleStatus": [
      
    ]
  }