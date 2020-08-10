"""
This file (test_socket.py) contains the functional tests for checking
socket events and operations
"""
import json

import pytest

import hydrus.data.crud as crud
from hydrus.tests.conftest import gen_dummy_object


@pytest.mark.usefixtures('init_db_for_socket_tests')
class TestSocket:
    def test_connect(self, socketio, app, session):
        """Test connect event."""
        socket_client = socketio.test_client(app, namespace='/sync')
        data = socket_client.get_received('/sync')
        assert len(data) > 0
        event = data[0]
        assert event['name'] == 'connect'
        last_job_id = crud.get_last_modification_job_id(session)
        assert event['args'][0]['last_job_id'] == last_job_id
        socket_client.disconnect(namespace='/sync')

    def test_reconnect(self, socketio, app, session):
        """Test reconnect event."""
        socket_client = socketio.test_client(app, namespace='/sync')
        # Flush data of first connect event
        socket_client.get_received('/sync')
        # Client reconnects by emitting 'reconnect' event.
        socket_client.emit('reconnect', namespace='/sync')
        # Get update received on reconnecting to the server
        data = socket_client.get_received('/sync')
        assert len(data) > 0
        # Extract the event information
        event = data[0]
        assert event['name'] == 'connect'
        last_job_id = crud.get_last_modification_job_id(session)
        # Check last job id with last_job_id received by client in the update.
        assert event['args'][0]['last_job_id'] == last_job_id
        socket_client.disconnect(namespace='/sync')

    def test_modification_table_diff(self, socketio_client, session):
        """Test 'modification-table-diff' events."""
        # Flush old received data at socket client
        socketio_client.get_received('/sync')
        # Set last_job_id as the agent_job_id
        agent_job_id = crud.get_last_modification_job_id(session)
        # Add an extra modification record newer than the agent_job_id
        new_latest_job_id = crud.insert_modification_record(method='POST',
                                                            resource_url='', session=session)
        socketio_client.emit('get_modification_table_diff',
                             {'agent_job_id': agent_job_id}, namespace='/sync')
        data = socketio_client.get_received('/sync')
        assert len(data) > 0
        event = data[0]
        assert event['name'] == 'modification_table_diff'
        # Check received event contains data of newly added modification record.
        assert event['args'][0][0]['method'] == 'POST'
        assert event['args'][0][0]['resource_url'] == ''
        assert event['args'][0][0]['job_id'] == new_latest_job_id

    def test_socketio_POST_updates(self, socketio_client, test_app_client, constants, doc):
        """Test 'update' event emitted by socketio for POST operations."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get('/{}'.format(API_NAME))
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint not in ['@context', '@id', '@type', 'collections']:
                class_name = '/'.join(endpoints[endpoint].split(f'/{API_NAME}/')[1:])
                class_ = doc.parsed_classes[class_name]['class']
                class_methods = [x.method for x in class_.supportedOperation]
                if 'PUT' in class_methods:
                    # insert a object to be updated later
                    dummy_object = gen_dummy_object(class_.title, doc)
                    put_response = test_app_client.put(
                        endpoints[endpoint], data=json.dumps(dummy_object))
                    # extract id of the created object from the description of response
                    desc = put_response.json['description']
                    id_ = desc.split('ID ')[1].split(' successfully')[0]
                    # Flush old socketio updates
                    socketio_client.get_received('/sync')
                    # POST object
                    if 'POST' in class_methods:
                        new_dummy_object = gen_dummy_object(class_.title, doc)
                        post_response = test_app_client.post(
                            f'{endpoints[endpoint]}/{id_}',
                            data=json.dumps(new_dummy_object))
                        assert post_response.status_code == 200
                        # Get new socketio update
                        update = socketio_client.get_received('/sync')
                        assert len(update) != 0
                        assert update[0]['args'][0]['method'] == 'POST'
                        resource_name = update[0]['args'][0]['resource_url'].split('/')[-2]
                        assert resource_name == endpoints[endpoint].split('/')[-1]

    def test_socketio_DELETE_updates(self, socketio_client, test_app_client, constants, doc):
        """Test 'update' event emitted by socketio for DELETE operations."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get('/{}'.format(API_NAME))
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint not in ['@context', '@id', '@type', 'collections']:
                class_name = '/'.join(endpoints[endpoint].split(f'/{API_NAME}/')[1:])
                class_ = doc.parsed_classes[class_name]['class']
                class_methods = [x.method for x in class_.supportedOperation]
                if 'PUT' in class_methods:
                    # insert a object first to be deleted later
                    dummy_object = gen_dummy_object(class_.title, doc)
                    put_response = test_app_client.put(
                        endpoints[endpoint], data=json.dumps(dummy_object))
                    # extract id of the created object from the description of response
                    desc = put_response.json['description']
                    id_ = desc.split('ID ')[1].split(' successfully')[0]
                    # Flush old socketio updates
                    socketio_client.get_received('/sync')
                    if 'DELETE' in class_methods:
                        delete_response = test_app_client.delete(f'{endpoints[endpoint]}/{id_}')
                        assert delete_response.status_code == 200
                        # Get new update event
                        update = socketio_client.get_received('/sync')
                        assert len(update) != 0
                        assert update[0]['args'][0]['method'] == 'DELETE'
                        resource_name = update[0]['args'][0]['resource_url'].split('/')[-2]
                        assert resource_name == endpoints[endpoint].split('/')[-1]
