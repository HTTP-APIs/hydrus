"""API Doc generator for the server side API."""

from hydrus.hydraspec.doc_writer import HydraDoc, HydraClass, HydraClassProp, HydraClassOp
import json


def doc_gen(API: str, BASE_URL: str) -> HydraDoc:
    """Generate API Doc for server."""
    # Main API Doc
    api_doc = HydraDoc(API,
                       "API Doc for the server side API",
                       "API Documentation for the server side system",
                       API,
                       BASE_URL)

    # State Class
    state = HydraClass("State", "State", "Class for drone state objects")
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
                                        "vocab:State",
                                        [{"statusCode": 404, "description": "State not found"},
                                         {"statusCode": 200, "description": "State Returned"}]))

    # Drone Class
    drone = HydraClass("Drone", "Drone", "Class for a drone")
    # Properties
    drone.add_supported_prop(HydraClassProp(
        "vocab:State", "DroneState", False, False, True))
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
                                        "vocab:Drone",
                                        None,
                                        [{"statusCode": 200, "description": "Drone updated"}]))
    drone.add_supported_op(HydraClassOp("CreateDrone",
                                        "PUT",
                                        "vocab:Drone",
                                        None,
                                        [{"statusCode": 200, "description": "Drone added"}]))
    drone.add_supported_op(HydraClassOp("GetDrone",
                                        "GET",
                                        None,
                                        "vocab:Drone",
                                        [{"statusCode": 404, "description": "Drone not found"},
                                         {"statusCode": 200, "description": "Drone Returned"}]))

    # NOTE: Commands are stored in a collection. You may GET a command or you
    # may DELETE it, there is not UPDATE.
    command = HydraClass("Command", "Command", "Class for drone commands")
    command.add_supported_prop(HydraClassProp(
        "http://schema.org/identifier", "DroneID", False, False, True))
    command.add_supported_prop(HydraClassProp(
        "vocab:State", "State", False, False, True))
    # Used by mechanics to get newly added commands
    command.add_supported_op(HydraClassOp("GetCommand",
                                          "GET",
                                          None,
                                          "vocab:Command",
                                          [{"statusCode": 404, "description": "Command not found"},
                                           {"statusCode": 200, "description": "Command Returned"}]))
    # Used by server to add new commands
    command.add_supported_op(HydraClassOp("AddCommand",
                                          "PUT",
                                          "vocab:Command",
                                          None,
                                          [{"statusCode": 201, "description": "Command added"}]))

    command.add_supported_op(HydraClassOp("DeleteCommand",
                                          "DELETE",
                                          None,
                                          None,
                                          [{"statusCode": 201, "description": "Command deleted"}]))

    # Logs to be accessed mostly by the GUI. Mechanics should add logs for
    # every event.
    log = HydraClass("LogEntry", "LogEntry", "Class for a log entry")
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
        "vocab:State", "State", False, True, False))
    log.add_supported_prop(HydraClassProp(
        "vocab:Datastream", "Data", False, True, False))
    log.add_supported_prop(HydraClassProp(
        "vocab:Command", "Command", False, True, False))
    # GUI will get a certain log entry.
    log.add_supported_op(HydraClassOp("GetLog",
                                      "GET",
                                      None,
                                      "vocab:LogEntry",
                                      [{"statusCode": 404, "description": "Log entry not found"},
                                       {"statusCode": 200, "description": "Log entry returned"}]))
    log.add_supported_op(HydraClassOp("AddLog",
                                      "PUT",
                                      "vocab:LogEntry",
                                      None,
                                      [{"statusCode": 201, "description": "Log entry created"}]))

    # Data is stored as a collection. Each data object can be read.
    # New data added to the collection
    datastream = HydraClass("Datastream", "Datastream",
                            "Class for a datastream entry")
    datastream.add_supported_prop(HydraClassProp(
        "http://schema.org/QuantitativeValue", "Temperature", False, False, True))
    datastream.add_supported_prop(HydraClassProp(
        "http://schema.org/identifier", "DroneID", False, False, True))
    datastream.add_supported_prop(HydraClassProp(
        "http://schema.org/geo", "Position", False, False, True))
    datastream.add_supported_op(HydraClassOp("ReadDatastream",
                                             "GET",
                                             None,
                                             "vocab:Datastream",
                                             [{"statusCode": 404, "description": "Data not found"},
                                              {"statusCode": 200, "description": "Data returned"}]))
    datastream.add_supported_op(HydraClassOp("UpdateDatastream",
                                             "POST",
                                             "vocab:Datastream",
                                             None,
                                             [{"statusCode": 200, "description": "Data updated"}]))
    datastream.add_supported_op(HydraClassOp("DeleteDatastream",
                                             "DELETE",
                                             None,
                                             None,
                                             [{"statusCode": 200, "description": "Data deleted"}]))

    # Single object representing the area of interest. No collections.
    area = HydraClass(
        "Area", "Area", "Class for Area of Interest of the server", endpoint=True)
    # Using two positions to have a bounding box
    area.add_supported_prop(HydraClassProp(
        "http://schema.org/geo", "TopLeft", False, False, True))
    area.add_supported_prop(HydraClassProp(
        "http://schema.org/geo", "BottomRight", False, False, True))
    # Allowing updation of the area of interest
    area.add_supported_op(HydraClassOp("UpdateArea",
                                       "POST",
                                       "vocab:Area",
                                       None,
                                       [{"statusCode": 200, "description": "Area of interest changed"}]))
    area.add_supported_op(HydraClassOp("GetArea",
                                       "GET",
                                       None,
                                       "vocab:Area",
                                       [{"statusCode": 404, "description": "Area of interest not found"},
                                        {"statusCode": 200, "description": "Area of interest returned"}]))

    message = HydraClass("Message", "Message",
                         "Class for messages received by the GUI interface")
    message.add_supported_prop(HydraClassProp(
        "http://schema.org/Text", "MessageString", False, False, True))
    message.add_supported_op(HydraClassOp("GetMessage",
                                          "GET",
                                          None,
                                          "vocab:Message",
                                          [{"statusCode": 404, "description": "Message not found"},
                                           {"statusCode": 200, "description": "Message returned"}]))
    message.add_supported_op(HydraClassOp("DeleteMessage",
                                          "DELETE",
                                          None,
                                          None,
                                          [{"statusCode": 200, "description": "Message deleted"}]))

    api_doc.add_supported_class(drone, collection=True)
    api_doc.add_supported_class(state, collection=True)
    api_doc.add_supported_class(datastream, collection=True)
    api_doc.add_supported_class(log, collection=True)
    api_doc.add_supported_class(area, collection=False)
    api_doc.add_supported_class(command, collection=True)
    api_doc.add_supported_class(message, collection=True)

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
