"""API Doc generator for the server side API."""

import json

from hydra_python_core.doc_writer import (HydraClass, HydraClassOp,
                                          HydraClassProp, HydraDoc,
                                          HydraStatus, HydraCollection)


def doc_gen(API: str, BASE_URL: str) -> HydraDoc:
    """Generate API Doc for server."""
    # Main API Doc
    api_doc = HydraDoc(API,
                       "API Doc for the server side API",
                       "API Documentation for the server side system",
                       API,
                       BASE_URL,
                       "vocab")

    # State Class
    state = HydraClass("State", "Class for drone state objects", endpoint=True)
    # Properties
    state.add_supported_prop(HydraClassProp(
        "http://auto.schema.org/speed", "Speed", False, False, True))
    state.add_supported_prop(HydraClassProp(
        "http://schema.org/geo", "Position", False, False, True))
    state.add_supported_prop(HydraClassProp(
        "http://schema.org/Property", "Direction", False, False, True))
    state.add_supported_prop(HydraClassProp(
        "http://schema.org/fuelCapacity", "Battery", False, False, True))
    state.add_supported_prop(HydraClassProp(
        "https://schema.org/status", "SensorStatus", False, False, True))
    state.add_supported_prop(HydraClassProp(
        "http://schema.org/identifier", "DroneID", False, False, True))
    # Operations
    state.add_supported_op(HydraClassOp("GetState",
                                        "GET",
                                        None,
                                        state.id_,
                                        possible_status=[HydraStatus(code=404, desc="State not found"),
                                                         HydraStatus(code=200, desc="State Returned")]))
    state_collection_manages = {
        "property": "rdfs:type",
        "object": state.id_
    }
    state_collection = HydraCollection(collection_name="StateCollection",
                                       collection_description="A collection of states",
                                       manages=state_collection_manages)
    # Drone Class
    drone = HydraClass("Drone", "Class for a drone", endpoint=True)
    # Properties
    drone.add_supported_prop(HydraClassProp(
        state.id_, "DroneState", False, False, True))
    drone.add_supported_prop(HydraClassProp(
        "http://schema.org/name", "name", False, False, True))
    drone.add_supported_prop(HydraClassProp(
        "http://schema.org/model", "model", False, False, True))
    drone.add_supported_prop(HydraClassProp(
        "http://auto.schema.org/speed", "MaxSpeed", False, False, True))
    drone.add_supported_prop(HydraClassProp(
        "http://schema.org/device", "Sensor", False, False, True))
    # Operations
    # Drones will submit their state to the server at certain intervals or
    # when some event happens
    drone.add_supported_op(HydraClassOp("SubmitDrone",
                                        "POST",
                                        drone.id_,
                                        None,
                                        possible_status=[HydraStatus(code=200, desc="Drone updated")]))
    drone.add_supported_op(HydraClassOp("CreateDrone",
                                        "PUT",
                                        drone.id_,
                                        None,
                                        possible_status=[HydraStatus(code=200, desc="Drone added")]))
    drone.add_supported_op(HydraClassOp("GetDrone",
                                        "GET",
                                        None,
                                        drone.id_,
                                        possible_status=[HydraStatus(code=404, desc="Drone not found"),
                                                         HydraStatus(code=200, desc="Drone Returned")]))
    drone_collection_manages = {
        "property": "rdfs:type",
        "object": drone.id_
    }
    drone_collection = HydraCollection(collection_name="DroneCollection",
                                         collection_description="A collection of drones",
                                         manages=drone_collection_manages)

    # NOTE: Commands are stored in a collection. You may GET a command or you
    # may DELETE it, there is not UPDATE.
    command = HydraClass("Command", "Class for drone commands", endpoint=True)
    command.add_supported_prop(HydraClassProp(
        "http://schema.org/identifier", "DroneID", False, False, True))
    command.add_supported_prop(HydraClassProp(
        state.id_, "State", False, False, True))
    # Used by mechanics to get newly added commands
    command.add_supported_op(HydraClassOp("GetCommand",
                                          "GET",
                                          None,
                                          command.id_,
                                          possible_status=[HydraStatus(code=404, desc="Command not found"),
                                                           HydraStatus(code=200, desc="Command Returned")]))
    # Used by server to add new commands
    command.add_supported_op(HydraClassOp("AddCommand",
                                          "PUT",
                                          command.id_,
                                          None,
                                          possible_status=[HydraStatus(code=201, desc="Command added")]))

    command.add_supported_op(HydraClassOp("DeleteCommand",
                                          "DELETE",
                                          None,
                                          None,
                                          possible_status=[HydraStatus(code=201, desc="Command deleted")]))
    command_collection_manages = {
        "property": "rdfs:type",
        "object": command.id_
    }
    command_collection = HydraCollection(collection_name="CommandCollection",
                                         collection_description="A collection of commands",
                                         manages=command_collection_manages)

    # Data is stored as a collection. Each data object can be read.
    # New data added to the collection
    datastream = HydraClass("Datastream",
                            "Class for a datastream entry", endpoint=True)
    datastream.add_supported_prop(HydraClassProp(
        "http://schema.org/QuantitativeValue", "Temperature", False, False, True))
    datastream.add_supported_prop(HydraClassProp(
        "http://schema.org/identifier", "DroneID", False, False, True))
    datastream.add_supported_prop(HydraClassProp(
        "http://schema.org/geo", "Position", False, False, True))
    datastream.add_supported_op(HydraClassOp("ReadDatastream",
                                             "GET",
                                             None,
                                             datastream.id_,
                                             possible_status=[HydraStatus(code=404, desc="Data not found"),
                                             HydraStatus(code=200, desc="Data returned")]))
    datastream.add_supported_op(HydraClassOp("UpdateDatastream",
                                             "POST",
                                             datastream.id_,
                                             None,
                                             possible_status=[HydraStatus(code=200, desc="Data updated")]))
    datastream.add_supported_op(HydraClassOp("DeleteDatastream",
                                             "DELETE",
                                             None,
                                             None,
                                             possible_status=[HydraStatus(code=200, desc="Data deleted")]))
    datastream_collection_manages = {
        "property":"rdfs:type",
        "object" : datastream.id_
    }
    datastream_collection = HydraCollection(collection_name="DatastreamCollection",
                                            collection_description="A collection of datastream",
                                            manages=datastream_collection_manages)

    # Logs to be accessed mostly by the GUI. Mechanics should add logs for
    # every event.
    log = HydraClass("LogEntry", "Class for a log entry", endpoint=True)
    # Subject
    log.add_supported_prop(HydraClassProp(
        "http://schema.org/identifier", "DroneID", True, True, False))
    # Predicate
    log.add_supported_prop(HydraClassProp(
        "http://schema.org/UpdateAction", "Update", False, True, False))
    log.add_supported_prop(HydraClassProp(
        "http://schema.org/ReplyAction", "Get", False, True, False))
    log.add_supported_prop(HydraClassProp(
        "http://schema.org/SendAction", "Send", False, True, False))
    # Objects
    log.add_supported_prop(HydraClassProp(
        state.id_, "State", False, True, False))
    log.add_supported_prop(HydraClassProp(
        datastream.id_, "Data", False, True, False))
    log.add_supported_prop(HydraClassProp(
        command.id_, "Command", False, True, False))
    # GUI will get a certain log entry.
    log.add_supported_op(HydraClassOp("GetLog",
                                      "GET",
                                      None,
                                      log.id_,
                                      possible_status=[HydraStatus(code=404, desc="Log entry not found"),
                                                       HydraStatus(code=200, desc="Log entry returned")]))
    log.add_supported_op(HydraClassOp("AddLog",
                                      "PUT",
                                      log.id_,
                                      None,
                                      possible_status=[HydraStatus(code=201, desc="Log entry created")]))
    log_collection_manages = {
        "property": "rdfs:type",
        "object": log.id_
    }
    log_collection = HydraCollection(collection_name="LogEntryCollection",
                                            collection_description="A collection of logs",
                                            manages=log_collection_manages)

    # Single object representing the area of interest. No collections.
    area = HydraClass( "Area", "Class for Area of Interest of the server", endpoint=True)
    # Using two positions to have a bounding box
    area.add_supported_prop(HydraClassProp(
        "http://schema.org/geo", "TopLeft", False, False, True))
    area.add_supported_prop(HydraClassProp(
        "http://schema.org/geo", "BottomRight", False, False, True))
    # Allowing updation of the area of interest
    area.add_supported_op(HydraClassOp("UpdateArea",
                                       "POST",
                                       area.id_,
                                       None,
                                       possible_status=[HydraStatus(code=200,
                                                                    desc="Area of interest changed")]))
    area.add_supported_op(HydraClassOp("GetArea",
                                       "GET",
                                       None,
                                       area.id_,
                                       possible_status=[HydraStatus(code=200, desc="Area of interest not found"),
                                                        HydraStatus(code=200, desc="Area of interest returned")]))

    message = HydraClass("Message",
                         "Class for messages received by the GUI interface", endpoint=True)
    message.add_supported_prop(HydraClassProp(
        "http://schema.org/Text", "MessageString", False, False, True))
    message.add_supported_op(HydraClassOp("GetMessage",
                                          "GET",
                                          None,
                                          message.id_,
                                          possible_status=[HydraStatus(code=200, desc="Message not found"),
                                                           HydraStatus(code=200, desc="Message returned")]))
    message.add_supported_op(HydraClassOp("DeleteMessage",
                                          "DELETE",
                                          None,
                                          None,
                                          possible_status=[HydraStatus(code=200, desc="Message deleted")]))
    message_collection_manages = {
        "property": "rdfs:type",
        "object": message.id_
    }
    message_collection = HydraCollection(collection_name="MessageCollection",
                                         collection_description="A collection of messages",
                                         manages=message_collection_manages)

    api_doc.add_supported_class(drone)
    api_doc.add_supported_collection(drone_collection)
    api_doc.add_supported_class(state)
    api_doc.add_supported_collection(state_collection)
    api_doc.add_supported_class(datastream)
    api_doc.add_supported_collection(datastream_collection)
    api_doc.add_supported_class(log)
    api_doc.add_supported_collection(log_collection)
    api_doc.add_supported_class(area)
    api_doc.add_supported_class(command)
    api_doc.add_supported_collection(command_collection)
    api_doc.add_supported_class(message)
    api_doc.add_supported_collection(message_collection)

    api_doc.add_baseResource()
    api_doc.add_baseCollection()
    api_doc.gen_EntryPoint()
    return api_doc


if __name__ == "__main__":
    dump = json.dumps(
        doc_gen("api", "http://localhost:8080/").generate(), indent=4, sort_keys=True)
    doc = '''"""\nGenerated API Documentation for Server API using server_doc_gen.py."""\n\ndoc = %s''' % dump
    doc = doc.replace('true', '"true"')
    doc = doc.replace('false', '"false"')
    doc = doc.replace('null', '"null"')
    f = open("doc.py", "w")
    f.write(doc)
    f.close()
