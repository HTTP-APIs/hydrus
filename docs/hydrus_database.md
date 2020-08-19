## hydrus

`hydrus` is a core part of the HydraEcosystem. It is the server which powers Hydra-based API Docs.

We are going to see the main steps `hydrus` performs when it is given an API doc and has to start the server:

1) As the given API doc is a python `dict`, `hydrus` uses the `hydra-python-core` library to parse it. Therefore all the heavy lifting of parsing the API doc is handled by the core library. The core library returns a convinent `apidoc` object which `hydrus` uses further.  The core library returns an expanded API doc.
    > The `apidoc` object exposes all the relevant details of the given API doc in a nice API. For example, we can get the all parsed classes by just doing `apidoc.parsed_classes` or we can get all collections by doing `apidoc.collections`.
2) After we have the `apidoc` object, the next big task for `hydrus` is to setup the database. The schema for the database of `hydrus` is specific to the given API doc. That means it convinently makes a database architecture which optimizes for the given API doc.
The overview of the process of making a database from `apidoc` object is:
-  Go through all the parsed classes (`apidoc.parsed_classes`) and all the collections (`apidoc.collections`) and make a table for each.
	> Parsed classes is the set of all classes in the API doc for which a database table is necessary. This just means all the classes in API doc except the classes defining `hydra:Collection` (`@id` is `http://www.w3.org/ns/hydra/core#Collection`), `hydra:Resource`(`@id` is `http://www.w3.org/ns/hydra/core#Resource`) and the EntryPoint class.

- For a parsed class, the columns are all the properties in `supportedProperty` for that class in the API doc. These can be found from `apidoc.parsed_classes['class_name']['class'].supportedProperty`. If any of the property is referring to another class in the same API doc, that column will be treated as a foreign key to that class. Therefore that column will store the `id`(primary key) of the other table. For any other general property, there will just be a simple column for that. If the property is a `hydra:Link`, that will **not** be treated as a foreign key because its a link, the duty of linking falls on the client rather that the server.  
- The table for a collection is slightly different from a parsed_class. Any collection will have only 4 columns. Those are `id`(primary key), `members`(this is used for storing the `id` of the instance of the class that the collection *manages*), `collection_id` which is the id for any collection the user creates and `member_type` which is used to store the `@type` of the member.
	> A collection is defined as a "set of somehow related resources".

3) After the database is made,`hydrus` creates a Flask app. It enables required properties like authentication, pagination, etc and then starts the server.
