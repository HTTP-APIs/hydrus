"""API Doc templates generator."""


class HydraDoc():
    """Class for an API Doc."""

    def __init__(self, API, title, desc, entrypoint, base_url):
        """Initialize the APIDoc."""
        self.API = API
        self.title = title
        self.base_url = base_url
        self.context = Context(base_url + API)
        self.parsed_classes = dict()
        self.other_classes = list()
        self.collections = dict()
        self.status = list()
        self.entrypoint = HydraEntryPoint(base_url, entrypoint)
        self.desc = desc

    def add_supported_class(self, class_, collection=False, collectionGet=True, collectionPost=True):
        """Add a new supportedClass."""
        # self.doc["supportedClass"].append(class_.get())
        self.parsed_classes[class_.title] = {
            "context": Context(address=self.base_url+self.API, class_=class_),
            "class": class_
        }
        if collection:
            collection = HydraCollection(class_, collectionGet, collectionPost)
            self.collections[collection.name] = {
                "context": Context(address=self.base_url+self.API, collection=collection),
                "collection": collection
            }

    def add_possible_status(self, status):
        """Add a new possibleStatus."""
        self.status.append(status)

    def add_baseCollection(self):
        """Add Collection class to the API Doc."""
        collection = HydraClass("http://www.w3.org/ns/hydra/core#Collection", "Collection", None)
        member = HydraClassProp("http://www.w3.org/ns/hydra/core#member", "members", False, False, None)
        collection.add_supported_prop(member)
        self.other_classes.append(collection)

    def add_baseResource(self):
        """Add Resource class to the API Doc."""
        resource = HydraClass("http://www.w3.org/ns/hydra/core#Resource", "Resource", None)
        self.other_classes.append(resource)

    def add_to_context(self, key, value):
        """Add entries to the vocabs context."""
        self.context.add(key, value)

    def gen_EntryPoint(self):
        """Generate the EntryPoint for the Hydra Doc."""
        # pdb.set_trace()
        for class_ in self.parsed_classes:
            if self.parsed_classes[class_]["class"].endpoint:
                self.entrypoint.add_Class(self.parsed_classes[class_]["class"])
        for collection in self.collections:
            self.entrypoint.add_Collection(self.collections[collection]["collection"])

    def generate(self):
        """Get the Hydra API Doc as a python dict."""
        parsed_classes = [self.parsed_classes[key]["class"] for key in self.parsed_classes]
        collections = [self.collections[key]["collection"] for key in self.collections]
        doc = {
            "@context": self.context.generate(),
            "@id": self.base_url + self.API + "/vocab",
            "@type": "ApiDocumentation",
            "description": self.desc,
            "supportedClass": [x.generate() for x in parsed_classes + self.other_classes + collections + [self.entrypoint]],
            "possibleStatus": [x.generate() for x in self.status]
        }
        return doc


class HydraClass():
    """Template for a new class."""

    def __init__(self, id_, title, desc,  endpoint=False, sub_classof=None):
        """Initialize the Hydra_Class."""
        self.id_ = id_ if "http" in id_ else "vocab:"+id_
        self.title = title
        self.desc = desc
        self.parents = None
        self.endpoint = endpoint
        self.supportedProperty = list()
        self.supportedOperation = list()
        if sub_classof is not None:
            self.parents = sub_classof

    def add_supported_prop(self, prop):
        """Add a new supportedProperty."""
        self.supportedProperty.append(prop)

    def add_supported_op(self, op):
        """Add a new supportedOperation."""
        self.supportedOperation.append(op)

    def generate(self):
        """Get the Hydra class as a python dict."""
        class_ = {
            "@id": self.id_,
            "@type": "hydra:Class",
            "title": self.title,
            "description": self.desc,
            "supportedProperty": [x.generate() for x in self.supportedProperty],
            "supportedOperation": [x.generate() for x in self.supportedOperation],
        }
        if self.parents is not None:
            class_["subClassOf"] = self.parents
        return class_


class HydraClassProp():
    """Template for a new property."""

    def __init__(self, prop, title, read, write, required, desc=""):
        """Initialize the Hydra_Prop."""
        self.prop = prop
        self.title = title
        self.read = read
        self.write = write
        self.required = required
        self.desc = desc

    def generate(self):
        """Get the Hydra prop as a python dict."""
        prop = {
          "@type": "SupportedProperty",
          "title": self.title,
          "property": self.prop,
          "required": self.required,
          "readonly": self.read,
          "writeonly": self.write
        }
        if len(self.desc) > 0:
            prop["description"] = self.desc
        return prop


class HydraClassOp():
    """Template for a new supportedOperation."""

    def __init__(self, title, method, expects, returns, status):
        """Initialize the Hydra_Prop."""
        self.title = title
        self.method = method
        self.expects = expects
        self.returns = returns
        self.status = status

    def generate(self):
        """Get the Hydra op as a python dict."""
        op = {
                "@type": "hydra:Operation",
                "title": self.title,
                "method": self.method,
                "expects": self.expects,
                "returns": self.returns,
                "possibleStatus": self.status
        }
        return op


class HydraCollection():
    """Class for Hydra Collection."""

    def __init__(self, class_, get=True, post=True):
        """Generate Collection for a given class."""
        self.class_ = class_
        self.name = class_.title + "Collection"
        self.supportedOperation = list()
        self.supportedProperty = [HydraClassProp("http://www.w3.org/ns/hydra/core#member",
                                                 "members",
                                                 False, False, False,
                                                 "The %s" % (self.class_.title.lower()))]

        if get:
            get_op = HydraCollectionOp("_:%s_collection_retrieve" % (self.class_.title.lower()),
                                       "hydra:Operation",
                                       "GET", "Retrieves all %s entities" % (self.class_.title),
                                       None, "vocab:%s" % (self.name), [])
            self.supportedOperation.append(get_op)

        if post:
            post_op = HydraCollectionOp("_:%s_create" % (self.class_.title.lower()),
                                        "http://schema.org/AddAction",
                                        "POST", "Create new %s entitity" % (self.class_.title),
                                        self.class_.id_, self.class_.id_,
                                        [{"code": 201,
                                         "description": "If the %s entity was created successfully." % (self.class_.title)}]
                                        )
            self.supportedOperation.append(post_op)

    def generate(self):
        """Get as a python dict."""
        collection = {
            "@id": "vocab:%s" % (self.name,),
            "@type": "hydra:Class",
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "label": "%s" % (self.name),
            "description": "A collection of %s" % (self.class_.title.lower()),
            "supportedOperation": [x.generate() for x in self.supportedOperation],
            "supportedProperty": [x.generate() for x in self.supportedProperty]
        }
        return collection


class HydraCollectionOp():
    """Operation class for Collection operations."""

    def __init__(self, id_, type_, method, label, expects, returns, status=[]):
        """Create method."""
        self.id_ = id_
        self.type_ = type_
        self.method = method
        self.label = label
        self.returns = returns
        self.expects = expects
        self.status = status

    def generate(self):
        """Get as a Python dict."""
        object_ = {
            "@id": self.id_,
            "@type": self.type_,
            "method": self.method,
            "label": self.label,
            "expects": self.expects,
            "returns": self.returns,
            "statusCodes": self.status
        }
        return object_


class HydraEntryPoint():
    """Template for a new entrypoint."""

    def __init__(self, base_url, entrypoint):
        """Initialize the Entrypoint."""
        self.url = base_url
        self.api = entrypoint
        self.entrypoint = HydraClass("EntryPoint", "EntryPoint", "The main entry point or homepage of the API.")
        self.entrypoint.add_supported_op(EntryPointOp("_:entry_point", "GET", "The APIs main entry point.", None, None, "vocab:EntryPoint"))
        self.context = Context(base_url+entrypoint, entrypoint=self)

    def add_Class(self, class_):
        """Add supportedProperty to the EntryPoint."""
        entrypoint_class = EntryPointClass(class_)
        self.entrypoint.add_supported_prop(entrypoint_class)
        self.context.add(entrypoint_class.name, {"@id": entrypoint_class.id_, "@type": "@id"})

    def add_Collection(self, collection):
        """Add supportedProperty to the EntryPoint."""
        entrypoint_collection = EntryPointCollection(collection)
        self.entrypoint.add_supported_prop(entrypoint_collection)
        self.context.add(entrypoint_collection.name, {"@id": entrypoint_collection.id_, "@type": "@id"})

    def generate(self):
        """Get as a Python dict."""
        return self.entrypoint.generate()

    def get(self):
        """Create the EntryPoint object to be returnd for the get function."""
        object_ = {
            "@context": "/"+self.api+"/"+"contexts/EntryPoint.jsonld",
            "@id": "/"+self.api,
            "@type": "EntryPoint",
        }
        for item in self.entrypoint.supportedProperty:
            uri = item.id_
            object_[item.name] = uri.replace("vocab:EntryPoint", '/'+self.api)
        return object_


class Context():
    """Class for JSON-LD context."""

    def __init__(self, address, adders={}, class_=None, collection=None, entrypoint=None):
        """Initialize context."""
        # NOTE: adders is a dictionary containing additional context elements to the base Hydra context
        if class_ is not None:
            self.context = {
                "vocab": address + "/vocab#",
                "hydra": "http://www.w3.org/ns/hydra/core#",
                "members": "http://www.w3.org/ns/hydra/core#member",
                "object": "http://schema.org/object",
            }
            self.context[class_.title] = class_.id_
            for prop in class_.supportedProperty:
                self.context[prop.title] = prop.prop

        elif collection is not None:
            self.context = {
                "vocab": address + "/vocab#",
                "hydra": "http://www.w3.org/ns/hydra/core#",
                "members": "http://www.w3.org/ns/hydra/core#member",
            }
            self.context[collection.name] = "vocab:"+collection.name
            self.context[collection.class_.title] = collection.class_.id_

        elif entrypoint is not None:
            self.context = {
                "EntryPoint": "vocab:EntryPoint",
                "vocab": address + "/vocab#"
            }

        else:
            self.context = {
                "hydra": "http://www.w3.org/ns/hydra/core#",
                "property": {
                    "@type": "@id",
                    "@id": "hydra:property"
                },
                "supportedClass": "hydra:supportedClass",
                "supportedProperty": "hydra:supportedProperty",
                "supportedOperation": "hydra:supportedOperation",
                "statusCodes": "hydra:statusCodes",
                "label": "rdfs:label",
                "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                "vocab": address + "/vocab#",
                # "vocab": "localhost/api/vocab#",
                "domain": {
                    "@type": "@id",
                    "@id": "rdfs:domain"
                },
                "ApiDocumentation": "hydra:ApiDocumentation",
                "range": {
                    "@type": "@id",
                    "@id": "rdfs:range"
                },
                "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                "title": "hydra:title",
                "expects": {
                    "@type": "@id",
                    "@id": "hydra:expects"
                },
                "returns": {
                    "@id": "hydra:returns",
                    "@type": "@id"
                },
                "readonly": "hydra:readonly",
                "writeonly": "hydra:writeonly",
                "possibleStatus": "hydra:possibleStatus",
                "required": "hydra:required",
                "method": "hydra:method",
                "statusCode": "hydra:statusCode",
                "description": "hydra:description",
                "subClassOf": {
                    "@id": "rdfs:subClassOf",
                    "@type": "@id"
                }
            }

    def createContext(self, object_):
        """Create the context for the given object."""
        if type(object_) is HydraClass:
            self.add(object_.title, object_.id)
            for prop in object_.supportedProperty:
                self.add(prop.title, self.prop)
        if type(object_) is HydraCollection:
            self.add(object_.name, "vocab:"+object_.name)
            self.add(object_.class_.title, object_.class_.id)

    def generate(self):
        """Get as a python dict."""
        return self.context

    def add(self, key, value):
        """Add entry to context."""
        self.context[key] = value


class EntryPointCollection():
    """Class for a Collection Entry to the EntryPoint object."""

    def __init__(self, collection):
        """Create method."""
        self.name = collection.name
        self.id_ = "vocab:EntryPoint/" + self.name

    def generate(self):
        """Get as a python dict."""
        object_ = {
            "property": {
                "@id": self.id_,
                "@type": "hydra:Link",
                "label": self.name,
                "description": "The %s collection" % (self.name,),
                "domain": "vocab:EntryPoint",
                "range": "vocab:%s" % (self.name,),
            },
            "hydra:title": self.name.lower(),
            "hydra:description": "The %s collection" % (self.name,),
            "required": None,
            "readonly": True,
            "writeonly": False
        }
        return object_


class EntryPointClass():
    """Class for a Operation Entry to the EntryPoint object."""

    def __init__(self, class_):
        """Create method."""
        self.name = class_.title
        self.desc = class_.desc
        self.supportedOperation = class_.supportedOperation
        self.id_ = "vocab:EntryPoint/" + self.name

    def generate(self):
        """Get as Python Dict."""
        object_ = {
            "property": {
                "@id": self.id_,
                "@type": "hydra:Link",
                "label": self.name,
                "description": self.desc,
                "domain": "vocab:EntryPoint",
                "range": "vocab:%s" % (self.name),
                "supportedOperation": []
            },
            "hydra:title": self.name.lower(),
            "hydra:description": "The %s Class" % (self.name),
            "required": None,
            "readonly": True,
            "writeonly": False
        }
        for op in self.supportedOperation:
            operation = EntryPointOp("_:"+op.title.lower(), op.method, op.title, None, op.expects, op.returns, op.status)
            object_["property"]["supportedOperation"].append(operation.generate())
        return object_


class EntryPointOp():
    """supportedOperation for EntryPoint."""

    def __init__(self, id_, method, label, desc, expects, returns, statusCodes=[]):
        """Create method."""
        self.id_ = id_
        self.method = method
        self.label = label
        self.desc = desc
        self.expects = expects
        self.returns = returns
        self.statusCodes = statusCodes

    def generate(self):
        """Get as Python Dict."""
        prop = {
            "@id": self.id_,
            "@type": "hydra:Operation",
            "method": self.method,
            "label": self.label,
            "description": self.desc,
            "expects": self.expects,
            "returns": self.returns,
            "statusCodes": self.statusCodes
        }
        return prop


class HydraStatus():
    """Class for possibleStatus in Hydra Doc."""

    def __init__(self, code, title, desc):
        """Create method."""
        self.code = code
        self.title = title
        self.desc = desc

    def generate(self):
        """Get as Python dict."""
        status = {
          "@context": "http://www.w3.org/ns/hydra/context.jsonld",
          "@type": "Status",
          "statusCode": self.code,
          "title": self.title,
          "description": self.desc,
        }
        return status
