"""
This file (test_crud.py) contains the unit tests for
CRUD operations in hydrus.data.crud.
"""
import random
import uuid

from hydra_python_core.doc_writer import HydraLink, DocUrl

import hydrus.data.crud as crud
from hydrus.data.exceptions import PropertyNotGiven
from hydrus.tests.conftest import gen_dummy_object


def test_crud_insert_response_is_str(drone_doc_parsed_classes, drone_doc, session,
                                     init_db_for_crud_tests):
    """Test CRUD insert response is string"""
    object_ = gen_dummy_object(random.choice(drone_doc_parsed_classes), drone_doc)
    id_ = str(uuid.uuid4())
    response = crud.insert(object_=object_, id_=id_, session=session)

    assert isinstance(response, str)


def test_crud_get_returns_correct_object(drone_doc_parsed_classes, drone_doc, session):
    """Test CRUD get returns correct object"""
    object_ = gen_dummy_object(random.choice(drone_doc_parsed_classes), drone_doc)
    id_ = str(uuid.uuid4())
    response = crud.insert(object_=object_, id_=id_, session=session)
    object_ = crud.get(id_=id_, type_=object_['@type'], session=session, api_name='api')
    assert isinstance(response, str)
    assert object_['@id'].split('/')[-1] == id_


def test_get_for_nested_obj(drone_doc_parsed_classes, drone_doc, session, constants):
    """Test CRUD get operation for object that can contain other objects."""
    expanded_base_url = DocUrl.doc_url
    for class_ in drone_doc_parsed_classes:
        for prop in drone_doc.parsed_classes[class_]['class'].supportedProperty:
            if not isinstance(prop.prop, HydraLink):
                if expanded_base_url in prop.prop:
                    dummy_obj = gen_dummy_object(class_, drone_doc)
                    nested_class = prop.prop.split(expanded_base_url)[1]
                    obj_id = str(uuid.uuid4())
                    response = crud.insert(object_=dummy_obj, id_=obj_id, session=session)
                    object_ = crud.get(id_=obj_id, type_=class_, session=session,
                                       api_name='api')
                    assert prop.title in object_
                    nested_obj_id = object_[prop.title]
                    nested_obj = crud.get(id_=nested_obj_id, type_=nested_class,
                                          session=session, api_name='api')
                    assert nested_obj['@id'].split('/')[-1] == nested_obj_id
                    break


def test_searching_over_collection_elements(drone_doc_parsed_classes, drone_doc, session):
    """Test searching over collection elements."""
    expanded_base_url = DocUrl.doc_url
    for class_ in drone_doc_parsed_classes:
        target_property_1 = ''
        target_property_2 = ''
        for prop in drone_doc.parsed_classes[class_]['class'].supportedProperty:
            if isinstance(prop.prop, HydraLink):
                continue
            # Find nested object so we can test searching of elements by
            # properties of nested objects.
            if expanded_base_url in prop.prop:
                object_ = gen_dummy_object(class_, drone_doc)
                # Setting property of a nested object as target
                for property_ in object_[prop.title]:
                    if property_ != '@type':
                        object_[prop.title][property_] = 'target_1'
                        target_property_1 = '{}[{}]'.format(
                            prop.title, property_)
                        break
                break
            elif target_property_1 is not '':
                for property_ in object_:
                    if property_ != '@type':
                        object_[property_] = 'target_2'
                        target_property_2 = property_
                        break
                break

            if target_property_1 is not '' and target_property_2 is not '':
                # Set search parameters
                search_params = {
                    target_property_1: 'target_1',
                    target_property_2: 'target_2'
                }

                obj_id = str(uuid.uuid4())
                response = crud.insert(
                    object_=object_, id_=obj_id, session=session)
                search_result = crud.get_collection(API_NAME='api', type_=class_,
                                                    session=session, paginate=True,
                                                    page_size=5, search_params=search_params)
                assert len(search_result['members']) > 0
                search_item_id = search_result['members'][0]['@id'].split(
                    '/')[-1]
                assert search_item_id == obj_id
                break


def test_update_on_object(drone_doc_parsed_classes, drone_doc, session):
    """Test CRUD update on object"""
    random_class = random.choice(drone_doc_parsed_classes)
    object_ = gen_dummy_object(random_class, drone_doc)
    new_object = gen_dummy_object(random_class, drone_doc)
    id_ = str(uuid.uuid4())
    insert_response = crud.insert(object_=object_, id_=id_, session=session)
    update_response = crud.update(
        id_=id_,
        type_=object_['@type'],
        object_=new_object,
        session=session,
        api_name='api')
    test_object = crud.get(id_=id_, type_=object_['@type'], session=session, api_name='api')
    assert isinstance(insert_response, str)
    assert isinstance(update_response, str)
    assert insert_response == update_response
    assert test_object['@id'].split('/')[-1] == id_


def test_delete_on_object(drone_doc_parsed_classes, drone_doc, session):
    """Test CRUD delete on object"""
    object_ = gen_dummy_object(random.choice(drone_doc_parsed_classes), drone_doc)
    id_ = str(uuid.uuid4())
    insert_response = crud.insert(object_=object_, id_=id_, session=session)
    assert isinstance(insert_response, str)
    delete_response = crud.delete(id_=id_, type_=object_['@type'], session=session)
    response_code = None
    try:
        get_response = crud.get(
            id_=id_,
            type_=object_['@type'],
            session=session,
            api_name='api')
    except Exception as e:
        error = e.get_HTTP()
        response_code = error.code
    assert 404 == response_code


def test_get_on_wrong_id(drone_doc_parsed_classes, drone_doc, session):
    """Test CRUD get when wrong/undefined ID is given."""
    id_ = str(uuid.uuid4())
    type_ = random.choice(drone_doc_parsed_classes)
    response_code = None
    try:
        get_response = crud.get(id_=id_, type_=type_, session=session, api_name='api')
    except Exception as e:
        error = e.get_HTTP()
        response_code = error.code
    assert 404 == response_code


def test_delete_on_wrong_id(drone_doc_parsed_classes, drone_doc, session):
    """Test CRUD delete when wrong/undefined ID is given."""
    object_ = gen_dummy_object(random.choice(
        drone_doc_parsed_classes), drone_doc)
    id_ = str(uuid.uuid4())
    insert_response = crud.insert(object_=object_, id_=id_, session=session)
    response_code = None
    try:
        delete_response = crud.delete(id_=999, type_=object_['@type'], session=session)
    except Exception as e:
        error = e.get_HTTP()
        response_code = error.code
    assert 404 == response_code
    assert isinstance(insert_response, str)
    assert insert_response == id_


def test_insert_used_id(drone_doc_parsed_classes, drone_doc, session):
    """Test CRUD insert when used ID is given."""
    object_ = gen_dummy_object(random.choice(drone_doc_parsed_classes), drone_doc)
    id_ = str(uuid.uuid4())
    insert_response = crud.insert(object_=object_, id_=id_, session=session)
    response_code = None
    try:
        insert_response = crud.insert(
            object_=object_, id_=id_, session=session)
    except Exception as e:
        error = e.get_HTTP()
        response_code = error.code
    assert 400 == response_code


def test_get_on_wrong_type(session):
    """Test CRUD get when wrong/undefined class is given."""
    id_ = str(uuid.uuid4())
    type_ = 'otherClass'
    response_code = None
    try:
        get_response = crud.get(id_=id_, type_=type_, session=session, api_name='api')
    except Exception as e:
        error = e.get_HTTP()
    assert 400 == error.code


def test_delete_on_wrong_type(drone_doc_parsed_classes, drone_doc, session):
    """Test CRUD delete when wrong/undefined class is given."""
    object_ = gen_dummy_object(random.choice(drone_doc_parsed_classes), drone_doc)
    id_ = str(uuid.uuid4())
    insert_response = crud.insert(object_=object_, id_=id_, session=session)
    assert isinstance(insert_response, str)
    assert insert_response == id_
    response_code = None
    try:
        delete_response = crud.delete(id_=id_, type_='otherClass', session=session)
    except Exception as e:
        error = e.get_HTTP()
        response_code = error.code
    assert 400 == response_code


def test_insert_on_wrong_type(drone_doc_parsed_classes, drone_doc, session):
    """Test CRUD insert when wrong/undefined class is given."""
    object_ = gen_dummy_object(random.choice(drone_doc_parsed_classes), drone_doc)
    id_ = str(uuid.uuid4())
    object_['@type'] = 'otherClass'
    response_code = None
    try:
        insert_response = crud.insert(object_=object_, id_=id_, session=session)
    except Exception as e:
        error = e.get_HTTP()
        response_code = error.code
    assert 400 == response_code


def test_insert_multiple_id(drone_doc_parsed_classes, drone_doc, session):
    """Test CRUD insert when multiple ID's are given """
    objects = list()
    ids = '{},{}'.format(str(uuid.uuid4()), str(uuid.uuid4()))
    ids_list = ids.split(',')
    for index in range(len(ids_list)):
        object = gen_dummy_object(random.choice(drone_doc_parsed_classes), drone_doc)
        objects.append(object)
    insert_response = crud.insert_multiple(objects_=objects, session=session, id_=ids)
    for id_ in ids_list:
        assert id_ in insert_response


def test_delete_multiple_id(drone_doc_parsed_classes, drone_doc, session):
    """Test CRUD insert when multiple ID's are given """
    objects = list()
    ids = '{},{}'.format(str(uuid.uuid4()), str(uuid.uuid4()))
    random_class = random.choice(drone_doc_parsed_classes)
    for index in range(len(ids.split(','))):
        object = gen_dummy_object(random_class, drone_doc)
        objects.append(object)
    insert_response = crud.insert_multiple(objects_=objects, session=session, id_=ids)
    delete_response = crud.delete_multiple(id_=ids, type_=random_class, session=session)

    response_code = None
    id_list = ids.split(',')
    try:
        for index in range(len(id_list)):
            get_response = crud.get(
                id_=id_list[index],
                type_=objects[index]['@type'],
                session=session,
                api_name='api')
    except Exception as e:
        error = e.get_HTTP()
        response_code = error.code
    assert 404 == response_code


def test_insert_when_property_not_given(drone_doc_parsed_classes, drone_doc,
                                        session, constants):
    """Test CRUD insert operation when a required foreign key
    property of that resource(column in the table) not given"""
    expanded_base_url = DocUrl.doc_url
    for class_ in drone_doc_parsed_classes:
        for prop in drone_doc.parsed_classes[class_]['class'].supportedProperty:
            if not isinstance(prop.prop, HydraLink) and expanded_base_url in prop.prop:
                dummy_obj = gen_dummy_object(class_, drone_doc)
                nested_prop_title = prop.title
                continue
    # remove the foreign key resource on purpose for testing
    dummy_obj.pop(nested_prop_title)
    id_ = str(uuid.uuid4())
    try:
        insert_response = crud.insert(object_=dummy_obj, id_=id_, session=session)
    except PropertyNotGiven as e:
        error = e.get_HTTP()
        response_code = error.code
        assert 400 == response_code
