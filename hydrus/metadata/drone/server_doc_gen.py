"""API Doc generator for the server side API."""

from hydrus.hydraspec.doc_writer import HydraDoc, HydraClass, HydraClassProp, HydraClassOp
import json


def server_doc(API, BASE_URL):
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
    state.add_supported_prop(HydraClassProp("http://auto.schema.org/speed", "Speed", True, False, False))
    state.add_supported_prop(HydraClassProp("http://schema.org/geo", "Position", True, False, False))
    state.add_supported_prop(HydraClassProp("http://schema.org/fuelCapacity", "Battery", True, True, False))
    state.add_supported_prop(HydraClassProp("https://schema.org/status", "SensorStatus", True, False, False))

    # Drone Class
    drone = HydraClass("Drone", "Drone", "Class for a drone")
    # Properties
    drone.add_supported_prop(HydraClassProp("vocab:State", "DroneState", True, False, False))
    drone.add_supported_prop(HydraClassProp("http://schema.org/name", "name", True, False, False))
    drone.add_supported_prop(HydraClassProp("http://schema.org/model", "model", True, False, False))
    drone.add_supported_prop(HydraClassProp("http://auto.schema.org/speed", "MaxSpeed", True, False, False))
    drone.add_supported_prop(HydraClassProp("http://schema.org/device", "Sensor", True, True, False))
    # Operations
    # Drones will submit their state to the server at certain intervals or when some event happens
    drone.add_supported_op(HydraClassOp("SubmitState",
                                        "POST",
                                        "vocab:State",
                                        None,
                                        [{"statusCode": 200, "description": "Drone State updated"}]))
    # Mechanics or GUI need to get the drone, it contains the state object of the drone already.
    drone.add_supported_op(HydraClassOp("GetDrone",
                                        "GET",
                                        None,
                                        "vocab:Drone",
                                        [{"statusCode": 404, "description": "Drone not found"},
                                         {"statusCode": 200, "description": "Drone Returned"}]))

    # No need for endpoint. Server mechanics will create and add send them to the drone
    command = HydraClass("Command", "Command", "Class for drone commands")
    command.add_supported_prop(HydraClassProp("http://schema.org/UpdateAction", "Update", False, True, False))
    command.add_supported_prop(HydraClassProp("vocab:State", "State", False, False, False))

    # Logs to be accessed mostly by the GUI. Mechanics should add logs for every event.
    log = HydraClass("vocab:LogEntry", "LogEntry", "Class for a log entry")
    # Subject
    log.add_supported_prop(HydraClassProp("http://schema.org/identifier", "DroneID", True, True, False))
    # Predicate
    log.add_supported_prop(HydraClassProp("http://schema.org/UpdateAction", "Update", False, True, False))
    log.add_supported_prop(HydraClassProp("http://schema.org/ReplyAction", "Get", False, True, False))
    log.add_supported_prop(HydraClassProp("http://schema.org/SendAction", "Send", False, True, False))
    # Objects
    log.add_supported_prop(HydraClassProp("vocab:State", "State", False, True, False))
    log.add_supported_prop(HydraClassProp("vocab:Data", "Data", False, True, False))
    log.add_supported_prop(HydraClassProp("vocab:Command", "Command", False, True, False))
    # GUI will get a certain log entry.
    log.add_supported_op(HydraClassOp("GetLog",
                                      "GET",
                                      None,
                                      "vocab:LogEntry",
                                      [{"statusCode": 404, "description": "Log entry not found"},
                                       {"statusCode": 200, "description": "Log entry returned"}]))

    # Data is stored as a collection. Each data object can be read.
    # New data added to the collection
    data = HydraClass("vocab:Data", "Data", "Class for a data entry")
    data.add_supported_prop(HydraClassProp("http://schema.org/QuantitativeValue", "Temperature", True, False, False))
    data.add_supported_prop(HydraClassProp("http://schema.org/identifier", "DroneID", True, False, False))
    data.add_supported_prop(HydraClassProp("http://schema.org/geo", "Position", True, False, False))
    data.add_supported_op(HydraClassOp("ReadData",
                                       "GET",
                                       None,
                                       "vocab:Data",
                                       [{"statusCode": 404, "description": "Data not found"},
                                        {"statusCode": 200, "description": "Data returned"}]))

    # Single object representing the area of interest. No collections.
    area = HydraClass("vocab:Area", "Area", "Class for Area of Interest of the server", endpoint=True)
    # Using two positions to have a bounding box
    area.add_supported_prop(HydraClassProp("http://schema.org/geo", "TopLeft", True, True, True))
    area.add_supported_prop(HydraClassProp("http://schema.org/geo", "BottomRight", True, True, True))
    # Allowing updation of the area of interest
    area.add_supported_op(HydraClassOp("UpdateArea",
                                       "PUT",
                                       "vocab:Area",
                                       None,
                                       [{"statusCode": 200, "description": "Area of interest changed"}]))
    area.add_supported_op(HydraClassOp("GetArea",
                                       "GET",
                                       None,
                                       "vocab:Area",
                                       [{"statusCode": 404, "description": "Area of interest not found"},
                                        {"statusCode": 200, "description": "Area of interest returned"}]))

    message = HydraClass("vocab:Message", "Message", "Class for messages received by the GUI interface")
    message.add_supported_prop(HydraClassProp("http://schema.org/Text", "MessageString", True, True, False))
    message.add_supported_op(HydraClassOp("GetMessage",
                                          "GET",
                                          None,
                                          "vocab:Message",
                                          [{"statusCode": 404, "description": "Message not found"},
                                           {"statusCode": 200, "description": "Message returned"}]))

    api_doc.add_supported_class(drone, collection=True)
    api_doc.add_supported_class(state, collection=False)
    api_doc.add_supported_class(data, collection=True)
    api_doc.add_supported_class(log, collection=True)
    api_doc.add_supported_class(area, collection=False)
    api_doc.add_supported_class(command, collection=False)
    api_doc.add_supported_class(message, collection=True)

    api_doc.add_baseResource()
    api_doc.add_baseCollection()
    api_doc.gen_EntryPoint()
    return api_doc


if __name__ == "__main__":
    dump = json.dumps(server_doc("serverapi", "http://localhost/").generate(), indent=4, sort_keys=True)
    doc = '''"""Generated API Documentation for Server API using server_doc_gen.py."""\n\nserver_doc = %s''' % dump
    doc = doc.replace('true', '"true"')
    doc = doc.replace('false', '"false"')
    doc = doc.replace('null', '"null"')
    f = open("server_doc.py", "w")
    f.write(doc)
    f.close()
