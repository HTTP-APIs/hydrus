"""API Doc generator for the server side API."""

from hydrus.hydraspec.doc_writer import HydraDoc, HydraClass, HydraClassProp, HydraClassOp
import pprint

def doc_gen(API, BASE_URL):
    """Generate API Doc for server."""
    # Main API Doc
    api_doc = HydraDoc(API,
                       "API Doc for the server side API",
                       "API Documentation for the server side system",
                       API,
                       BASE_URL)

    # Status Class
    status = HydraClass("Status", "Status", "Class for drone status objects")
    # Properties
    status.add_supported_prop(HydraClassProp("http://auto.schema.org/speed", "Speed", True, False, False))
    status.add_supported_prop(HydraClassProp("http://schema.org/geo", "Position", True, False, False))
    status.add_supported_prop(HydraClassProp("http://schema.org/fuelCapacity", "Battery", True, True, False))
    status.add_supported_prop(HydraClassProp("https://schema.org/status", "SensorStatus", True, False, False))

    # Drone Class
    drone = HydraClass("Drone", "Drone", "Class for a drone")
    # Properties
    drone.add_supported_prop(HydraClassProp("vocab:Status", "DroneStatus", True, False, False))
    drone.add_supported_prop(HydraClassProp("http://schema.org/name", "name", True, False, False))
    drone.add_supported_prop(HydraClassProp("http://schema.org/model", "model", True, False, False))
    drone.add_supported_prop(HydraClassProp("http://auto.schema.org/speed", "MaxSpeed", True, False, False))
    drone.add_supported_prop(HydraClassProp("http://schema.org/device", "Sensor", True, True, False))
    # Operations
    drone.add_supported_op(HydraClassOp("SubmitStatus",
                                        "PUT",
                                        "vocab:Status",
                                        None,
                                        [{"statusCode": 200, "description": "Drone Status updated"}]))
    drone.add_supported_op(HydraClassOp("GetDrone",
                                        "GET",
                                        None,
                                        "vocab:Drone",
                                        [{"statusCode": 200, "description": "Drone Returned"}]))

    command = HydraClass("Command", "Command", "Class for drone commands")
    command.add_supported_prop(HydraClassProp("http://schema.org/UpdateAction", "Update", False, True, False))
    command.add_supported_prop(HydraClassProp("vocab:Status", "Status", False, False, False))

    log = HydraClass("LogEntry", "LogEntry", "Class for a log entry")
    # Subject
    log.add_supported_prop(HydraClassProp("http://schema.org/identifier", "DroneID", True, True, False))
    # Predicate
    log.add_supported_prop(HydraClassProp("http://schema.org/UpdateAction", "Update", False, True, False))
    log.add_supported_prop(HydraClassProp("http://schema.org/ReplyAction", "Get", False, True, False))
    log.add_supported_prop(HydraClassProp("http://schema.org/SendAction", "Send", False, True, False))
    # Objects
    log.add_supported_prop(HydraClassProp("vocab:Status", "Status", False, True, False))
    log.add_supported_prop(HydraClassProp("vocab:Data", "Data", False, True, False))
    log.add_supported_prop(HydraClassProp("vocab:Command", "Command", False, True, False))
    log.add_supported_op(HydraClassOp("GetLog",
                                      "GET",
                                      None,
                                      "voab:LogEntry",
                                      [{"statusCode": 404, "description": "Log entry not found"},
                                       {"statusCode": 200, "description": "Log entry returned"}]))

    data = HydraClass("Data", "Data", "Class for a data entry")
    data.add_supported_prop(HydraClassProp("http://schema.org/QuantitativeValue", "Temperature", True, False, False))
    data.add_supported_prop(HydraClassProp("http://schema.org/identifier", "DroneID", True, False, False))
    data.add_supported_prop(HydraClassProp("http://schema.org/geo", "Position", True, False, False))
    data.add_supported_op(HydraClassOp("ReadData",
                                       "GET",
                                       None,
                                       "vocab:Data",
                                       [{"statusCode": 404, "description": "Data not found"},
                                        {"statusCode": 200, "description": "Data returned"}]))
    data.add_supported_op(HydraClassOp("SubmitData",
                                       "POST",
                                       "vocab:Data",
                                       None,
                                       [{"statusCode": 201, "description": "Data added"}]))

    area = HydraClass("Area", "Area", "Class for Area of Interest of the server", endpoint=True)
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
                                       [{"statusCode": 404, "description": "Area of not found"},
                                        {"statusCode": 200, "description": "Area of returned"}]))

    message = HydraClass("Message", "Message", "Class for messages received by the GUI interface")
    message.add_supported_prop(HydraClassProp("http://schema.org/Text", "MessageString", True, True, False))

    api_doc.add_supported_class(drone, collection=True)
    api_doc.add_supported_class(status, collection=True)
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
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(doc_gen("serverapi", "").generate())
