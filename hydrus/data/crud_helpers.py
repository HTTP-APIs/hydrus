# from sqlalchemy.orm.session import Session
from sqlalchemy.orm.scoping import scoped_session
from typing import Dict, Any, Tuple

from sqlalchemy.orm.exc import NoResultFound
from hydrus.data.db_models import (Graph, BaseProperty, RDFClass, Instance,
                                   Terminal)
from hydrus.data.exceptions import (
    PageNotFound,
    InvalidSearchParameter,
    IncompatibleParameters,
    OffsetOutOfRange)


def apply_filter(object_id: str, search_props: Dict[str, Any],
                 triples: Graph, session: scoped_session) -> bool:
    """Check whether objects has properties with query values or not.
    :param object_id: Id of the instance.
    :param search_props: Dictionary of query parameters with property id and values.
    :param triples: All triples.
    :param session: sqlalchemy scoped session.
    :return: True if the instance has properties with given values, False otherwise.
    """
    for prop in search_props:
        # For nested properties
        if isinstance(search_props[prop], dict):
            data = session.query(triples).filter(
                triples.GraphIII.subject == object_id, triples.GraphIII.predicate == prop).one()
            if apply_filter(data.object_, search_props[prop], triples, session) is False:
                return False
        else:
            data = session.query(triples).filter(
                triples.GraphIIT.subject == object_id, triples.GraphIIT.predicate == prop).one()
            terminal = session.query(Terminal).filter(
                Terminal.id == data.object_).one()
            if terminal.value != search_props[prop]:
                return False
    return True


def recreate_iri(API_NAME: str, path: str, search_params: Dict[str, Any]) -> str:
    """Recreate the IRI with query arguments
    :param API_NAME: API name specified while starting the server.
    :param path: endpoint
    :param search_params: List of query parameters.
    :return: Recreated IRI.
    """
    iri = "/{}/{}?".format(API_NAME, path)
    for param in search_params:
        # Skip page, pageIndex or offset parameters as they will be updated to point to
        # next, previous and last page
        if param == "page" or param == "pageIndex" or param == "offset":
            continue
        iri += "{}={}&".format(param, search_params[param])
    return iri


def parse_search_params(search_params: Dict[str, Any],
                        properties: BaseProperty,
                        session: scoped_session) -> Dict[str, Any]:
    """Parse search parameters and create a dict with id of parameters as keys.
    :param search_params: Dictionary having input search parameters.
    :param properties: All properties.
    :param session: sqlalchemy session.
    :return: A dictionary having property ids as keys.
    """
    search_props = dict()
    pagination_parameters = ["page", "pageIndex", "limit", "offset"]
    for param in search_params:
        # Skip if the parameter is a pagination parameter
        if param in pagination_parameters:
            continue
        # For one level deep nested parameters
        if "[" in param and "]" in param:
            prop_name = param.split('[')[0]
            try:
                prop_id = session.query(properties).filter(
                    properties.name == prop_name).one().id
                if prop_id not in search_props:
                    search_props[prop_id] = {}
                nested_prop_id = session.query(properties).filter(
                    properties.name == param[param.find('[') + 1:param.find(']')]).one().id
                search_props[prop_id][nested_prop_id] = search_params[param]
            except NoResultFound:
                raise InvalidSearchParameter(param)
        # For normal parameters
        else:
            try:
                prop_id = session.query(properties).filter(
                    properties.name == param).one().id
                search_props[prop_id] = search_params[param]
            except NoResultFound:
                raise InvalidSearchParameter(param)
    return search_props


def calculate_page_limit_and_offset(paginate: bool, page_size: int, page: int, result_length: int,
                                    offset: int, limit: int) -> Tuple[int, int]:
    """Calculate page limit and offset for pagination.
    :param paginate: Showing whether pagination is enable/disable.
    :param page_size: Number maximum elements showed in a page.
    :param page: page number.
    :param result_length: Length of the list containing desired elements.
    :param offset: offset value.
    :param limit: page limit.
    :return: page limit and offset.
    """
    if limit is not None:
        page_size = limit
    if paginate is True:
        if offset is None:
            offset = (page - 1) * page_size
        limit = page_size
    else:
        offset = 0
        limit = result_length

    return limit, offset


def pre_process_pagination_parameters(search_params: Dict[str, Any], paginate: bool,
                                      page_size: int, result_length: int) -> Tuple[int, int, int]:
    """Pre-process pagination related query parameters passed by client.
    :param search_params: Dict of all search parameters.
    :param paginate: Indicates if pagination is enabled/disabled.
    :param page_size: Maximum element a page can contain.
    :param result_length: Length of the list of containing desired items.
    :return: returns page number, page limit and offset.
    """
    incompatible_parameters = ["page", "pageIndex", "offset"]
    incompatible_parameters_len = len(incompatible_parameters)
    # Find any pair of incompatible parameters
    for i in range(incompatible_parameters_len):
        if incompatible_parameters[i] not in search_params:
            continue
        if i != incompatible_parameters_len - 1:
            for j in range(i+1, incompatible_parameters_len):
                if incompatible_parameters[j] in search_params:
                    raise IncompatibleParameters([incompatible_parameters[i],
                                                  incompatible_parameters[j]])
    try:
        # Extract page number from query arguments
        if "pageIndex" in search_params:
            page = int(search_params.get("pageIndex"))
            offset = None
        elif "offset" in search_params:
            offset = int(search_params.get("offset"))
            page = offset//page_size + 1
            if offset > result_length:
                raise OffsetOutOfRange(str(offset))
        else:
            page = int(search_params.get("page", 1))
            offset = None
        if "limit" in search_params:
            limit = int(search_params.get("limit"))
        else:
            limit = None
    except ValueError:
        raise PageNotFound(page)
    page_limit, offset = calculate_page_limit_and_offset(paginate=paginate, page_size=page_size,
                                                         page=page, result_length=result_length,
                                                         offset=offset, limit=limit)
    return page, page_limit, offset


def attach_hydra_view(collection_template: Dict[str, Any], paginate_param: str,
                      result_length: int, page_size: int,
                      iri: str, offset: int = None,
                      page: int = None, last: int = None) -> None:
    """Attaches hydra:view to the collection template.
    :param collection_template: the collection template.
    :param paginate_param: type of paginate parameter used.
    :param result_length: length of the result set.
    :param page_size: size of the page.
    :param iri: IRI of the collection with query parameters except "page", "pageIndex" and "offset".
    :param offset: offset used for pagination, None if not used.
    :param page: page number used for pagination, None if not used.
    :param last: Page number of the last page only used when "page" or "pageIndex"
                 is used for pagination, None otherwise.
    """
    if paginate_param == "offset":
        collection_template["view"] = {
            "@id": "{}{}={}".format(iri, paginate_param, offset),
            "@type": "PartialCollectionView",
            "first": "{}{}=0".format(iri, paginate_param),
            "last": "{}{}={}".format(iri, paginate_param, result_length-page_size)
        }
        if offset > page_size:
            collection_template["view"]["previous"] = "{}{}={}".format(iri,
                                                                       paginate_param,
                                                                       offset - page_size)
        if offset < result_length-page_size:
            collection_template["view"]["next"] = "{}{}={}".format(iri,
                                                                   paginate_param,
                                                                   offset + page_size)
    else:
        collection_template["view"] = {
            "@id": "{}{}={}".format(iri, paginate_param, page),
            "@type": "PartialCollectionView",
            "first": "{}{}=1".format(iri, paginate_param),
            "last": "{}{}={}".format(iri, paginate_param, last)
        }
        if page != 1:
            collection_template["view"]["previous"] = "{}{}={}".format(iri, paginate_param,
                                                                       page-1)
        if page != last:
            collection_template["view"]["next"] = "{}{}={}".format(iri, paginate_param,
                                                                   page + 1)
