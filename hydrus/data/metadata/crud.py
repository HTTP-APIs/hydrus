"""Basic CRUD operations for every Hydra Class."""


def template():
    """Template for supportedOperation."""
    supportedOperation = [
        {
            "@id": "_:%s_create",
            "@type": "hydra:Operation",
            "method": "POST",
            "label": "Creates a new %s entity",
            "description": "null",
            "expects": "%s",
            "returns": "%s",
            "statusCodes": [
            ]
        },
        {
            "@id": "_:%s_replace",
            "@type": "hydra:Operation",
            "method": "PUT",
            "label": "Replaces an existing %s entity",
            "description": "null",
            "expects": "%s",
            "returns": "%s",
            "statusCodes": [
                {
                    "code": 404,
                    "description": "If the %s entity wasn't found."
                }
            ]
        },
        {
            "@id": "_:%s_delete",
            "@type": "hydra:Operation",
            "method": "DELETE",
            "label": "Deletes a %s entity",
            "description": "null",
            "expects": "null",
            "returns": "null",
            "statusCodes": [
            ]
        },
        {
            "@id": "_:%s_retrieve",
            "@type": "hydra:Operation",
            "method": "GET",
            "label": "Retrieves a %s entity",
            "description": "null",
            "expects": "null",
            "returns": "%s",
            "statusCodes": [
                {
                    "code": 404,
                    "description": "If the %s entity wasn't found."
                }
            ]
        }
    ]
    return supportedOperation
