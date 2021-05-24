"""
This file (test_app.py) contains the functional tests for checking if the
response format is proper. Run tests/unit/test_crud.py before running this.
"""

import json
import re
import uuid

import pytest
from hydra_python_core.doc_writer import HydraLink, DocUrl

from hydrus.tests.conftest import gen_dummy_object
from hydrus.utils import get_doc


# specify common fixture for all tests
@pytest.mark.usefixtures('init_db_for_app_tests')
class TestApp():
    def test_Index(self, test_app_client, constants):
        """Test for the Index."""
        HYDRUS_SERVER_URL = constants['HYDRUS_SERVER_URL']
        API_NAME = constants['API_NAME']
        response_get = test_app_client.get(f'/{API_NAME}')
        endpoints = json.loads(response_get.data.decode('utf-8'))
        response_post = test_app_client.post(f'/{API_NAME}', data=dict(foo='bar'))
        response_put = test_app_client.put(f'/{API_NAME}', data=dict(foo='bar'))
        response_delete = test_app_client.delete(f'/{API_NAME}')
        assert '@context' in endpoints
        assert endpoints['@id'] == f'{HYDRUS_SERVER_URL}{API_NAME}'
        assert endpoints['@type'] == 'EntryPoint'
        assert response_get.status_code == 200
        assert response_post.status_code == 405
        assert response_put.status_code == 405
        assert response_delete.status_code == 405

    def test_EntryPoint_context(self, test_app_client, constants):
        """Test for the EntryPoint context."""
        API_NAME = constants['API_NAME']
        response_get = test_app_client.get(f'/{API_NAME}/contexts/EntryPoint.jsonld')
        response_get_data = json.loads(response_get.data.decode('utf-8'))
        response_post = test_app_client.post(f'/{API_NAME}/contexts/EntryPoint.jsonld', data={})
        response_delete = test_app_client.delete(f'/{API_NAME}/contexts/EntryPoint.jsonld')
        assert response_get.status_code == 200
        assert '@context' in response_get_data
        assert response_post.status_code == 405
        assert response_delete.status_code == 405

    def test_Vocab(self, test_app_client, constants):
        """Test the vocab."""
        API_NAME = constants['API_NAME']
        HYDRUS_SERVER_URL = constants['HYDRUS_SERVER_URL']
        vocab_route = get_doc().doc_name
        response_get = test_app_client.get(f'/{API_NAME}/{vocab_route}#')
        response_get_data = json.loads(response_get.data.decode('utf-8'))

        assert '@context' in response_get_data
        assert response_get_data['@type'] == 'ApiDocumentation'
        assert response_get_data['@id'] == f'{HYDRUS_SERVER_URL}{API_NAME}/{vocab_route}'
        assert response_get.status_code == 200

        response_delete = test_app_client.delete(f'/{API_NAME}/{vocab_route}#')
        assert response_delete.status_code == 405

        response_put = test_app_client.put(
            f'/{API_NAME}/{vocab_route}#', data=json.dumps(dict(foo='bar')))
        assert response_put.status_code == 405

        response_post = test_app_client.post(f'/{API_NAME}/{vocab_route}#',
                                             data=json.dumps(dict(foo='bar')))
        assert response_post.status_code == 405

    def test_fragments(self, test_app_client, constants):
        """Test the fragments in vocab."""
        API_NAME = constants['API_NAME']
        HYDRUS_SERVER_URL = constants['HYDRUS_SERVER_URL']
        vocab_route = get_doc().doc_name
        response_get = test_app_client.get(f'/{API_NAME}/{vocab_route}#')
        response_get_data = json.loads(response_get.data.decode('utf-8'))

        for class_ in response_get_data['supportedClass']:
            resource_id = class_['@id']
            regex = "#[a-zA-Z]+"
            resource_name = re.search(regex, resource_id).group(0)
            resource_name = resource_name[1:]

            vocab_uri = f'{HYDRUS_SERVER_URL}{API_NAME}/{vocab_route}'
            param_string = f'?resource={resource_name}'
            response_fragment_get = test_app_client.get(f'{vocab_uri}{param_string}')
            response_fragment_get_data = json.loads(response_fragment_get.data.decode('utf-8'))

            assert response_fragment_get.status_code == 200
            assert '@context' in response_fragment_get_data
            assert response_fragment_get_data['supportedClass'][0]['@id'] == resource_id
            assert len(response_fragment_get_data['supportedClass']) == 1

    def test_Collections_GET(self, test_app_client, constants, doc, init_db_for_app_tests):
        """Test GET on collection endpoints."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints['collections']:
            response_get = test_app_client.get(endpoint['@id'])
            assert response_get.status_code == 200
            response_get_data = json.loads(response_get.data.decode('utf-8'))
            assert '@context' in response_get_data
            assert '@id' in response_get_data
            assert '@type' in response_get_data
            assert 'members' in response_get_data
            # Check the item URI has the valid format, so it can be dereferenced
            if len(response_get_data['members']) > 0:
                for item in response_get_data['members']:
                    class_type = item['@type']
                    if class_type in doc.parsed_classes:
                        class_ = doc.parsed_classes[class_type]['class']
                        class_methods = [
                            x.method for x in class_.supportedOperation]
                        if 'GET' in class_methods:
                            item_response = test_app_client.get(
                                response_get_data['members'][0]['@id'])
                            assert item_response.status_code == 200

    def test_pagination(self, test_app_client, constants, doc):
        """Test basic pagination"""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints['collections']:
            response_get = test_app_client.get(endpoint['@id'])
            assert response_get.status_code == 200
            response_get_data = json.loads(
                response_get.data.decode('utf-8'))
            assert 'hydra:view' in response_get_data
            assert 'hydra:first' in response_get_data['hydra:view']
            assert 'hydra:last' in response_get_data['hydra:view']
            if 'hydra:next' in response_get_data['hydra:view']:
                response_next = test_app_client.get(
                    response_get_data['hydra:view']['hydra:next'])
                assert response_next.status_code == 200
                response_next_data = json.loads(response_next.data.decode('utf-8'))
                assert 'hydra:previous' in response_next_data['hydra:view']
            break

    def test_Collections_PUT(self, test_app_client, constants, doc):
        """Test insert data to the collection."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints['collections']:
            collection_name = '/'.join(endpoint['@id'].split(f'/{API_NAME}/')[1:])
            collection = doc.collections[collection_name]['collection']
            collection_methods = [x.method for x in collection.supportedOperation]
            if 'PUT' in collection_methods:
                dummy_object = gen_dummy_object(collection.name, doc)
                good_response_put = test_app_client.put(endpoint['@id'],
                                                        data=json.dumps(dummy_object))
                assert good_response_put.status_code == 201
                assert good_response_put.json["iri"] == good_response_put.location

    def test_Collections_constraint_PUT(self, test_app_client, constants, doc):
        """Test collection constraints by inserting same object twice."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints['collections']:
            collection_name = '/'.join(endpoint['@id'].split(f'/{API_NAME}/')[1:])
            collection = doc.collections[collection_name]['collection']
            collection_methods = [x.method for x in collection.supportedOperation]
            if 'PUT' in collection_methods:
                dummy_object = gen_dummy_object(collection.name, doc)
                good_response_put = test_app_client.put(endpoint['@id'],
                                                        data=json.dumps(dummy_object))
                assert good_response_put.status_code == 201
                assert good_response_put.json["iri"] == good_response_put.location
                collection_id = good_response_put.location
                bad_response_put = test_app_client.put(collection_id,
                                                       data=json.dumps(dummy_object))
                assert bad_response_put.status_code == 400

    def test_collection_object_GET(self, test_app_client, constants, doc):
        """Test GET of a given collection object using ID."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints['collections']:
            collection_name = '/'.join(endpoint['@id'].split(f'/{API_NAME}/')[1:])
            collection = doc.collections[collection_name]['collection']
            collection_methods = [x.method for x in collection.supportedOperation]
            if 'PUT' in collection_methods:
                dummy_object = gen_dummy_object(collection.name, doc)
                initial_put_response = test_app_client.put(
                    endpoint['@id'], data=json.dumps(dummy_object))
                assert initial_put_response.status_code == 201
                response = json.loads(initial_put_response.data.decode('utf-8'))
                regex = r'(.*)ID (.{36})* (.*)'
                matchObj = re.match(regex, response['description'])
                assert matchObj is not None
                id_ = matchObj.group(2)
                if 'GET' in collection_methods:
                    get_response = test_app_client.get(f'{endpoint["@id"]}/{id_}')
                    assert get_response.status_code == 200

    def test_collection_object_PUT(self, test_app_client, constants, doc):
        """Test PUT of a given collection object using ID."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints['collections']:
            collection_name = '/'.join(endpoint['@id'].split(f'/{API_NAME}/')[1:])
            collection = doc.collections[collection_name]['collection']
            collection_methods = [x.method for x in collection.supportedOperation]
            if 'PUT' in collection_methods:
                dummy_object_1 = gen_dummy_object(collection.name, doc)
                initial_put_response = test_app_client.put(
                    endpoint['@id'], data=json.dumps(dummy_object_1))
                assert initial_put_response.status_code == 201
                collection_id = initial_put_response.location
                dummy_object_2 = gen_dummy_object(collection.name, doc)
                second_put_response = test_app_client.put(
                    collection_id, data=json.dumps(dummy_object_2))
                assert second_put_response.status_code == 201
                assert second_put_response.location == collection_id
                assert second_put_response.json["iri"] == collection_id

    def test_collection_object_POST(self, test_app_client, constants, doc, socketio):
        """Test POST of a given collection object using ID."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints['collections']:
            collection_name = '/'.join(endpoint['@id'].split(f'/{API_NAME}/')[1:])
            collection = doc.collections[collection_name]['collection']
            collection_methods = [x.method for x in collection.supportedOperation]
            dummy_object = gen_dummy_object(collection.name, doc)
            initial_put_response = test_app_client.put(
                endpoint['@id'], data=json.dumps(dummy_object))
            assert initial_put_response.status_code == 201
            assert initial_put_response.json["iri"] == initial_put_response.location
            response = json.loads(initial_put_response.data.decode('utf-8'))
            regex = r'(.*)ID (.{36})* (.*)'
            matchObj = re.match(regex, response['description'])
            assert matchObj is not None
            id_ = matchObj.group(2)
            if 'POST' in collection_methods:
                # members attribute should be writeable for POSTs
                if collection.supportedProperty[0].write:
                    dummy_object = gen_dummy_object(collection.name, doc)
                    post_replace_response = test_app_client.post(f'{endpoint["@id"]}/{id_}',
                                                                 data=json.dumps(dummy_object))
                    assert post_replace_response.status_code == 200

    def test_collection_object_DELETE(self, test_app_client, constants, doc):
        """Test DELETE of a given collection object using ID."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints['collections']:
            collection_name = '/'.join(
                endpoint["@id"].split(f'/{API_NAME}/')[1:])
            collection = doc.collections[collection_name]['collection']
            collection_methods = [
                x.method for x in collection.supportedOperation]
            dummy_object = gen_dummy_object(collection.name, doc)
            initial_put_response = test_app_client.put(endpoint["@id"],
                                                       data=json.dumps(dummy_object))
            assert initial_put_response.status_code == 201
            response = json.loads(initial_put_response.data.decode('utf-8'))
            regex = r'(.*)ID (.{36})* (.*)'
            matchObj = re.match(regex, response['description'])
            assert matchObj is not None
            id_ = matchObj.group(2)
            if 'DELETE' in collection_methods:
                delete_response = test_app_client.delete(
                    f'{endpoint["@id"]}/{id_}')
                assert delete_response.status_code == 200

    def test_object_PUT_at_id(self, test_app_client, constants, doc):
        """Create object in collection using PUT at specific ID."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints['collections']:
            collection_name = '/'.join(
                endpoint["@id"].split(f'/{API_NAME}/')[1:])
            collection = doc.collections[collection_name]['collection']
            collection_methods = [
                x.method for x in collection.supportedOperation]
            dummy_object = gen_dummy_object(collection.name, doc)
            if 'PUT' in collection_methods:
                dummy_object = gen_dummy_object(collection.name, doc)
                put_response = test_app_client.put(f'{endpoint["@id"]}/{uuid.uuid4()}',
                                                   data=json.dumps(dummy_object))
                assert put_response.status_code == 201
                assert put_response.json["iri"] == put_response.location

    def test_object_PUT_at_ids(self, test_app_client, constants, doc):
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint not in ['@context', '@id', '@type', 'collections']:
                class_name = '/'.join(endpoints[endpoint].split(f'/{API_NAME}/')[1:])
                if class_name not in doc.collections:
                    class_ = doc.parsed_classes[class_name]['class']
                    class_methods = [x.method for x in class_.supportedOperation]
                    data_ = {'data': list()}
                    objects = list()
                    ids = ''
                    for index in range(3):
                        objects.append(gen_dummy_object(class_.title, doc))
                        ids = f'{uuid.uuid4()},'
                    data_['data'] = objects
                    if 'PUT' in class_methods:
                        put_response = test_app_client.put(f'{endpoints[endpoint]}/add/{ids}',
                                                           data=json.dumps(data_))
                        assert put_response.status_code == 201
                        assert isinstance(put_response.json['iri'], list)

    def test_endpointClass_PUT(self, test_app_client, constants, doc):
        """Check non collection Class PUT."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint not in ['@context', '@id', '@type', 'collections']:
                class_name = '/'.join(
                    endpoints[endpoint].split(f'/{API_NAME}/')[1:])
                if class_name not in doc.collections:
                    class_ = doc.parsed_classes[class_name]['class']
                    class_methods = [
                        x.method for x in class_.supportedOperation]
                    if 'PUT' in class_methods:
                        dummy_object = gen_dummy_object(class_.title, doc)
                        put_response = test_app_client.put(endpoints[endpoint],
                                                           data=json.dumps(dummy_object))
                        assert put_response.status_code == 201
                        assert put_response.json["iri"] == put_response.location

    def test_endpointClass_POST(self, test_app_client, constants, doc):
        """Check non collection Class POST."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint not in ['@context', '@id', '@type', 'collections']:
                class_name = '/'.join(endpoints[endpoint].split(f'/{API_NAME}/')[1:])
                if class_name not in doc.collections:
                    class_ = doc.parsed_classes[class_name]['class']
                    class_methods = [x.method for x in class_.supportedOperation]
                    if 'PUT' in class_methods:
                        # first insert a object which we will update later
                        dummy_object = gen_dummy_object(class_.title, doc)
                        initial_put_response = test_app_client.put(endpoints[endpoint],
                                                                   data=json.dumps(dummy_object))
                        response = json.loads(
                            initial_put_response.data.decode('utf-8'))
                        regex = r'(.*)ID (.{36})* (.*)'
                        matchObj = re.match(regex, response['description'])
                        id_ = matchObj.group(2)
                        if 'POST' in class_methods:
                            dummy_object = gen_dummy_object(class_.title, doc)
                            post_response = test_app_client.post(f'{endpoints[endpoint]}/{id_}',
                                                                 data=json.dumps(dummy_object))
                            assert post_response.status_code == 200

    def test_endpointClass_DELETE(self, test_app_client, constants, doc):
        """Check non collection Class DELETE."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint not in ['@context', '@id', '@type', 'collections']:
                class_name = '/'.join(
                    endpoints[endpoint].split(f'/{API_NAME}/')[1:])
                if class_name not in doc.collections:
                    class_ = doc.parsed_classes[class_name]['class']
                    class_methods = [x.method for x in class_.supportedOperation]
                    if 'PUT' in class_methods:
                        # first insert a object which we will update later
                        dummy_object = gen_dummy_object(class_.title, doc)
                        initial_put_response = test_app_client.put(endpoints[endpoint],
                                                                   data=json.dumps(dummy_object))
                        response = json.loads(
                            initial_put_response.data.decode('utf-8'))
                        regex = r'(.*)ID (.{36})* (.*)'
                        matchObj = re.match(regex, response['description'])
                        id_ = matchObj.group(2)
                        if 'DELETE' in class_methods:
                            delete_response = test_app_client.delete(
                                f'{endpoints[endpoint]}/{id_}')
                            assert delete_response.status_code == 200

    def test_endpointClass_GET(self, test_app_client, constants, doc):
        """Check non collection Class GET."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint not in ['@context', '@id', '@type', 'collections']:
                class_name = '/'.join(endpoints[endpoint].split(f'/{API_NAME}/')[1:])
                if class_name not in doc.collections:
                    class_ = doc.parsed_classes[class_name]['class']
                    class_methods = [x.method for x in class_.supportedOperation]
                    if 'GET' in class_methods:
                        response_get = test_app_client.get(endpoints[endpoint])
                        assert response_get.status_code == 405

    def test_Collections_member_GET(self, test_app_client, constants, doc):
        """Test endpoint to get member from a collection"""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints['collections']:
            collection_name = '/'.join(endpoint['@id'].split(f'/{API_NAME}/')[1:])
            collection = doc.collections[collection_name]['collection']
            collection_methods = [x.method for x in collection.supportedOperation]
            if 'PUT' in collection_methods:
                dummy_object = gen_dummy_object(collection.name, doc)
                good_response_put = test_app_client.put(endpoint['@id'],
                                                        data=json.dumps(dummy_object))
                assert good_response_put.status_code == 201
                collection_endpoint = good_response_put.location
                if 'GET' in collection_methods:
                    for member in dummy_object['members']:
                        member_id = member['@id'].split('/')[-1]
                        get_response = test_app_client.get(f'{collection_endpoint}/{member_id}')
                        assert get_response.status_code == 200

    def test_Collections_member_DELETE(self, test_app_client, constants, doc):
        """Test endpoint to delete member from a collection."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints['collections']:
            collection_name = '/'.join(endpoint['@id'].split(f'/{API_NAME}/')[1:])
            collection = doc.collections[collection_name]['collection']
            collection_methods = [x.method for x in collection.supportedOperation]
            if 'PUT' in collection_methods:
                dummy_object = gen_dummy_object(collection.name, doc)
                good_response_put = test_app_client.put(endpoint['@id'],
                                                        data=json.dumps(dummy_object))
                assert good_response_put.status_code == 201
                collection_endpoint = good_response_put.location
                if 'DELETE' in collection_methods:
                    for member in dummy_object['members']:
                        member_id = member['@id'].split('/')[-1]
                        full_endpoint = f'{collection_endpoint}/{member_id}'
                        delete_response = test_app_client.delete(full_endpoint)
                        assert delete_response.status_code == 200

    def test_IriTemplate(self, test_app_client, constants, doc):
        """Test structure of IriTemplates attached to parsed classes"""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        expanded_base_url = DocUrl.doc_url
        for endpoint in endpoints['collections']:
            collection_name = '/'.join(endpoint["@id"].split(f'/{API_NAME}/')[1:])
            collection = doc.collections[collection_name]['collection']
            class_name = collection.manages["object"].split(expanded_base_url)[1]
            response_get = test_app_client.get(endpoint["@id"])
            assert response_get.status_code == 200
            response_get_data = json.loads(response_get.data.decode('utf-8'))
            assert 'search' in response_get_data
            assert 'hydra:mapping' in response_get_data['search']
            class_ = doc.parsed_classes[class_name]['class']
            class_props = [x.prop for x in class_.supportedProperty]
            for mapping in response_get_data['search']['hydra:mapping']:
                prop = mapping['hydra:property']
                prop_name = mapping['hydra:variable']
                is_valid_class_prop = prop not in ['limit', 'offset', 'pageIndex']
                # check if IRI property is for searching through a nested_class
                # and not this class_
                is_nested_class_prop = "[" in prop_name and "]" in prop_name
                if is_valid_class_prop and not is_nested_class_prop:
                    assert prop in class_props

    def test_client_controlled_pagination(self, test_app_client, constants, doc):
        """Test pagination controlled by test_app_client with help of pageIndex,
        offset and limit parameters."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints['collections']:
            response_get = test_app_client.get(endpoint["@id"])
            assert response_get.status_code == 200
            response_get_data = json.loads(response_get.data.decode('utf-8'))
            assert 'search' in response_get_data
            assert 'hydra:mapping' in response_get_data['search']
            # Test with pageIndex and limit
            params = {'pageIndex': 1, 'limit': 2}
            response_for_page_param = test_app_client.get(
                endpoint["@id"], query_string=params)
            assert response_for_page_param.status_code == 200
            response_for_page_param_data = json.loads(
                response_for_page_param.data.decode('utf-8'))
            assert 'hydra:first' in response_for_page_param_data['hydra:view']
            assert 'hydra:last' in response_for_page_param_data['hydra:view']
            if 'hydra:next' in response_for_page_param_data['hydra:view']:
                hydra_next = response_for_page_param_data['hydra:view']['hydra:next']
                assert 'pageIndex=2' in hydra_next
                next_response = test_app_client.get(
                    response_for_page_param_data['hydra:view']['hydra:next'])
                assert next_response.status_code == 200
                next_response_data = json.loads(
                    next_response.data.decode('utf-8'))
                assert 'hydra:previous' in next_response_data['hydra:view']
                data = next_response_data['hydra:view']['hydra:previous']
                assert 'pageIndex=1' in data
                # Test with offset and limit
                params = {'offset': 1, 'limit': 2}
                response_for_offset_param = test_app_client.get(endpoint["@id"],
                                                                query_string=params)
                assert response_for_offset_param.status_code == 200
                response_for_offset_param_data = json.loads(
                    response_for_offset_param.data.decode('utf-8'))
                data = response_for_offset_param_data['hydra:view']
                assert 'hydra:first' in data
                assert 'hydra:last' in data
                if 'hydra:next' in data:
                    assert 'offset=3' in data['hydra:next']
                    next_response = test_app_client.get(data['hydra:next'])
                    assert next_response.status_code == 200
                    next_response_data = json.loads(next_response.data.decode('utf-8'))
                    assert 'hydra:previous' in next_response_data['hydra:view']
                    assert 'offset=1' in next_response_data['hydra:view']['hydra:previous']

    def test_GET_for_nested_class(self, test_app_client, constants, doc):
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints['collections']:
            collection_name = '/'.join(endpoint["@id"].split(f'/{API_NAME}/')[1:])
            collection = doc.collections[collection_name]['collection']
            class_methods = [x.method for x in collection.supportedOperation]
            if 'GET' in class_methods:
                response_get = test_app_client.get(endpoint["@id"])
                assert response_get.status_code == 200
                instance = response_get.json['members'][0]['@id']
                instance_type = instance.split('/')[-2]
                instance_class = doc.parsed_classes[instance_type]['class']
                instance_methods = [x.method for x in instance_class.supportedOperation]
                if 'GET' in instance_methods:
                    response_get_data = test_app_client.get(instance).json
                    assert '@context' in response_get_data
                    assert '@id' in response_get_data
                    assert '@type' in response_get_data
                    class_props = [x for x in collection.supportedProperty]
                    expanded_base_url = DocUrl.doc_url
                    for prop_name in class_props:
                        if not isinstance(prop_name.prop, HydraLink):
                            if expanded_base_url in prop_name.prop:
                                assert '@type' in response_get_data[prop_name.title]

    def test_required_props(self, test_app_client, constants, doc):
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint not in ['@context', '@id', '@type', 'collections']:
                class_name = '/'.join(endpoints[endpoint].split(f'/{API_NAME}/')[1:])
                if class_name not in doc.collections:
                    class_ = doc.parsed_classes[class_name]['class']
                    class_methods = [x.method for x in class_.supportedOperation]
                    if 'PUT' in class_methods:
                        dummy_object = gen_dummy_object(class_.title, doc)
                        required_prop = ''
                        for prop in class_.supportedProperty:
                            if prop.required:
                                required_prop = prop.title
                                break
                        if required_prop:
                            del dummy_object[required_prop]
                            put_response = test_app_client.put(
                                endpoints[endpoint], data=json.dumps(dummy_object))
                            assert put_response.status_code == 400

    def test_writeable_props(self, test_app_client, constants, doc):
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint not in ['@context', '@id', '@type', 'collections']:
                class_name = '/'.join(endpoints[endpoint].split(f'/{API_NAME}/')[1:])
                if class_name not in doc.collections:
                    class_ = doc.parsed_classes[class_name]['class']
                    class_methods = [x.method for x in class_.supportedOperation]
                    if 'PUT' in class_methods:
                        # first insert a object which we will update later
                        dummy_object = gen_dummy_object(class_.title, doc)
                        initial_put_response = test_app_client.put(endpoints[endpoint],
                                                                   data=json.dumps(dummy_object))
                        response = json.loads(initial_put_response.data.decode('utf-8'))
                        regex = r'(.*)ID (.{36})* (.*)'
                        matchObj = re.match(regex, response['description'])
                        id_ = matchObj.group(2)
                        if 'POST' in class_methods:
                            dummy_object = gen_dummy_object(class_.title, doc)
                            # Test for writeable properties
                            post_response = test_app_client.post(
                                f'{endpoints[endpoint]}/{id_}', data=json.dumps(dummy_object))
                            assert post_response.status_code == 200
                            # Test for properties with writeable=False
                            non_writeable_prop = ''
                            for prop in class_.supportedProperty:
                                if prop.write is False:
                                    non_writeable_prop = prop.title
                                    break
                            if non_writeable_prop != '':
                                dummy_object[non_writeable_prop] = 'xyz'
                                post_response = test_app_client.post(
                                    endpoints[endpoint], data=json.dumps(dummy_object))
                                assert post_response.status_code == 405

    def test_readable_props(self, test_app_client, constants, doc):
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint not in ['@context', '@id', '@type', 'collections']:
                class_name = '/'.join(
                    endpoints[endpoint].split(f'/{API_NAME}/')[1:])
                if class_name not in doc.collections:
                    class_ = doc.parsed_classes[class_name]['class']
                    class_methods = [
                        x.method for x in class_.supportedOperation]
                    if 'GET' in class_methods:
                        not_readable_prop = ''
                        for prop in class_.supportedProperty:
                            if prop.read is False:
                                not_readable_prop = prop.title
                                break
                        if not_readable_prop:
                            get_response = test_app_client.get(
                                endpoints[endpoint])
                            get_response_data = json.loads(
                                get_response.data.decode('utf-8'))
                            assert not_readable_prop not in get_response_data

    def test_bad_objects(self, test_app_client, constants, doc):
        """Checks if bad objects are added or not."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint not in ['@context', '@id', '@type', 'collections']:
                class_name = '/'.join(
                    endpoints[endpoint].split(f'/{API_NAME}/')[1:])
                if class_name in doc.parsed_classes:
                    class_ = doc.parsed_classes[class_name]['class']
                    class_methods = [
                        x.method for x in class_.supportedOperation]
                    if 'PUT' in class_methods:
                        bad_response_put = test_app_client.put(
                            endpoints[endpoint],
                            data=json.dumps(dict(foo='bar')))
                        assert bad_response_put.status_code == 400

    def test_bad_requests(self, test_app_client, constants, doc):
        """Checks if bad requests are handled or not."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint not in ['@context', '@id', '@type', 'collections']:
                class_name = '/'.join(endpoints[endpoint].split(f'/{API_NAME}/')[1:])
                if class_name not in doc.collections:
                    class_ = doc.parsed_classes[class_name]['class']
                    class_methods = [x.method for x in class_.supportedOperation]
                    dummy_object = gen_dummy_object(class_.title, doc)
                    if 'PUT' in class_methods:
                        initial_put_response = test_app_client.put(
                            endpoints[endpoint], data=json.dumps(dummy_object))
                        assert initial_put_response.status_code == 201
                        response = json.loads(initial_put_response.data.decode('utf-8'))
                        regex = r'(.*)ID (.{36})* (.*)'
                        matchObj = re.match(regex, response['description'])
                        assert matchObj is not None
                        id_ = matchObj.group(2)
                        if 'POST' not in class_methods:
                            dummy_object = gen_dummy_object(class_.title, doc)
                            post_replace_response = test_app_client.post(
                                f'{endpoints[endpoint]}/{id_}', data=json.dumps(dummy_object))
                            assert post_replace_response.status_code == 405
                        if 'DELETE' not in class_methods:
                            delete_response = test_app_client.delete(
                                f'{endpoints[endpoint]}/{id_}')
                            assert delete_response.status_code == 405

    def test_Endpoints_Contexts(self, test_app_client, constants, doc):
        """Test all endpoints contexts are generated properly."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints['collections']:
            response_get = test_app_client.get(endpoints['@id'])
            assert response_get.status_code == 200
            context = json.loads(response_get.data.decode('utf-8'))['@context']
            response_context = test_app_client.get(context)
            response_context_data = json.loads(
                response_context.data.decode('utf-8'))
            assert response_context.status_code == 200
            assert '@context' in response_context_data
