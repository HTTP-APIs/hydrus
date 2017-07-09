parsed_classes = [
    {
         "@id":"http://schema.org/Order",
         "@type":"hydra:Class",
         "title":"Order",
         "description":"Handle orders from the central server.",
         "supportedOperation":[
            {
                "statusCodes": [
                    {
                        "code": 200,
                        "description": "Order successfully recieved."
                    }
                ],
                "@type": "http://schema.org/UpdateAction",
                "returns": "http://schema.org/Order",
                "label": "Recieves orders from the Central Server",
                "method": "PUT",
                "@id": "_:Order_create",
                "description": "null",
                "expects": "http://schema.org/Order"
            },
                        {
                            "statusCodes": [
                                {
                                    "code": 404,
                                    "description": "If no orders were found."
                                }
                            ],
                            "@type": "hydra:Operation",
                            "returns": "http://schema.org/Order",
                            "label": "Retrieves all orders from the central server.",
                            "method": "GET",
                            "@id": "_:Order_retrieve",
                            "description": "null",
                            "expects": "null"
                        }
         ],
         "supportedProperty":[

            {  "@type": "SupportedProperty",
               "property":"http://schema.org/geo",
               "title":"Destination",
               "hydra:description":"Coordinates of the new destination",
               "required":True,
               "readonly":False,
               "writeonly":False
            },
            {  "@type": "SupportedProperty",
               "property":"http://auto.schema.org/speed",
               "title":"Speed",
               "hydra:description":"Speed of Drone in Km/h",
               "required":True,
               "readonly":False,
               "writeonly":False
            },
         ]
      },

]
