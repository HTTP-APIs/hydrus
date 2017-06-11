"""
Generate documentation dictionaries.
"""

global_doc = {
  "@context": {
     "hydraspec": "http://www.w3.org/ns/hydraspec/context.jsonld",
  },
  "@id": "/api",
  "@type": "hydraspec:ApiDocumentation",
  "hydraspec:title": "Astronomical HYDRA",
  "hydraspec:description": "A demo API for HYDRA framework",
  "hydraspec:entrypoint": "/api",
  "hydraspec:supportedClass": [
    
  ],
  "hydraspec:possibleStatus": [
    
  ]
}

def make_doc(view):
  """
  Crate the dictionary for a given view (endpoint)
  """
  return {
    "@context": {
      "hydraspec": "http://www.w3.org/ns/hydraspec/context.jsonld"
    },
    "@id": "/api/hydraspec/{}".format(view),
    "@type": "hydraspec:ApiDocumentation",
    "hydraspec:title": "{}".format(view),
    "hydraspec:description": "",
    "hydraspec:entrypoint": "/api/{}".format(view),
    "hydraspec:supportedClass": [
      
    ],
    "hydraspec:possibleStatus": [
      
    ]
  }