"""
Generate documentation dictionaries.
"""

global_doc = {
  "@context": {
     "hydra": "http://www.w3.org/ns/hydra/context.jsonld",
  },
  "@id": "/api",
  "@type": "hydra:ApiDocumentation",
  "hydra:title": "Astronomical HYDRA",
  "hydra:description": "A demo API for HYDRA framework",
  "hydra:entrypoint": "/api",
  "hydra:supportedClass": [
    
  ],
  "hydra:possibleStatus": [
    
  ]
}

def make_doc(view):
  """
  Crate the dictionary for a given view (endpoint)
  """
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