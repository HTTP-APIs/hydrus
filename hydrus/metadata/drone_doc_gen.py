"""API Doc generator for the drone side API."""

from hydrus.hydraspec.doc_writer import HydraDoc, HydraClass, HydraClassProp, HydraClassOp
import json

# NOTE: @xadahiya: I'll add notes to different parts so that there is no confusion between Doc and Simulation

def drone_doc(API, BASE_URL):
    """Generate API Doc for drone."""
    # Main API Doc
    api_doc = HydraDoc(API,
                       "API Doc for the drone side API",
                       "API Documentation for the drone side system",
                       API,
                       BASE_URL)

    # State Class
    # NOTE: Each drone will have only one State Class, this can't be deleted. Only read and update.
    status = HydraClass("State", "State", "Class for drone status objects")
    # Properties
    status.add_supported_prop(HydraClassProp("http://auto.schema.org/speed", "Speed", True, False, False))
    status.add_supported_prop(HydraClassProp("http://schema.org/geo", "Position", True, False, False))
    status.add_supported_prop(HydraClassProp("http://schema.org/fuelCapacity", "Battery", True, True, False))
    status.add_supported_prop(HydraClassProp("https://schema.org/status", "SensorStatus", True, False, False))

    # Drone Class
    # NOTE: The actual changes to the drone are to be made at the /api/Drone URI.
    # GET will return current State. POST will update the State.
    drone = HydraClass("Drone", "Drone", "Class for a drone", endpoint=True)
    # Properties
    drone.add_supported_prop(HydraClassProp("vocab:State", "DroneState", True, False, False))
    drone.add_supported_prop(HydraClassProp("http://schema.org/name", "name", True, False, False))
    drone.add_supported_prop(HydraClassProp("http://schema.org/model", "model", True, False, False))
    drone.add_supported_prop(HydraClassProp("http://auto.schema.org/speed", "MaxSpeed", True, False, False))
    drone.add_supported_prop(HydraClassProp("http://schema.org/device", "Sensor", True, True, False))
    drone.add_supported_prop(HydraClassProp("http://schema.org/identifier", "DroneID", True, True, False))
    # Operations
    drone.add_supported_op(HydraClassOp("GetState",
                                        "GET",
                                        None,
                                        "vocab:State",
                                        [{"statusCode": 404, "description": "Data not found"},
                                         {"statusCode": 200, "description": "State Returned"}]))
    drone.add_supported_op(HydraClassOp("UpdateState",
                                        "POST",
                                        "vocab:State",
                                        None,
                                        [{"statusCode": 200, "description": "State updated"}]))

    # Command Class
    # NOTE: Commands are stored in a collection. You may GET a command or you may DELETE it, there is not UPDATE.
    command = HydraClass("Command", "Command", "Class for drone commands")
    command.add_supported_prop(HydraClassProp("http://schema.org/UpdateAction", "Update", False, True, False))
    command.add_supported_prop(HydraClassProp("http://hydrus.com/Status", "Status", False, False, False))
    command.add_supported_op(HydraClassOp("GetCommand",
                                          "GET",
                                          None,
                                          "vocab:Command",
                                          [{"statusCode": 404, "description": "Data not found"},
                                           {"statusCode": 200, "description": "Command Returned"}]))
    command.add_supported_op(HydraClassOp("DeleteCommand",
                                          "DELETE",
                                          None,
                                          None,
                                          [{"statusCode": 200, "description": "Command deleted"}]))

    # Data class
    # NOTE: This is for the Data to be captured/generated. The mechanics module will enter random data and POST it.
    # The server will read[GET] the data when it needs it. No need for collections. Only one instance showing current reading of sensor
    # The URI is /api/Data
    data = HydraClass("Data", "Data", "Class for a data entry", endpoint=True)
    data.add_supported_prop(HydraClassProp("http://schema.org/QuantitativeValue", "Temperature", True, False, False))
    data.add_supported_prop(HydraClassProp("http://schema.org/identifier", "DroneID", True, False, False))
    data.add_supported_prop(HydraClassProp("http://schema.org/geo", "Position", True, False, False))
    data.add_supported_op(HydraClassOp("GetData",
                                       "GET",
                                       None,
                                       "vocab:Data",
                                       [{"statusCode": 404, "description": "Data not found"},
                                        {"statusCode": 200, "description": "Data returned"}]))
    data.add_supported_op(HydraClassOp("UpdateData",
                                       "POST",
                                       "vocab:Data",
                                       None,
                                       [{"statusCode": 200, "description": "Data updated"}]))

    api_doc.add_supported_class(status, collection=False)
    api_doc.add_supported_class(drone, collection=False)
    api_doc.add_supported_class(command, collection=True)
    api_doc.add_supported_class(data, collection=False)

    api_doc.add_baseCollection()
    api_doc.add_baseResource()
    api_doc.gen_EntryPoint()
    return api_doc


if __name__ == "__main__":
    dump = json.dumps(drone_doc("droneapi", "http://localhost/").generate(), indent=4, sort_keys=True)
    doc = '''"""Generated API Documentation for Drone API using drone_doc_gen.py."""\n\ndrone_doc = %s''' % dump
    doc = doc.replace('true', '"true"')
    doc = doc.replace('false', '"false"')
    doc = doc.replace('null', '"null"')
    f = open("drone_doc.py", "w")
    f.write(doc)
    f.close()
