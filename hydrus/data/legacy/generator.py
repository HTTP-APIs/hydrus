"""Generate random objects for SubSystem classes."""

import random
from typing import Any, Dict, List, Optional

classes_keymap = {
    "communication": "Spacecraft_Communication",
    "propulsion": "Spacecraft_Propulsion",
    "detector": "Spacecraft_Detector",
    "primary power": "Spacecraft_PrimaryPower",
    "backup power": "Spacecraft_BackupPower",
    "thermal": "Spacecraft_Thermal",
    "structure":  "Spacecraft_Structure",
    "command and data": "Spacecraft_CDH",
    "attitude and orbit control": "Spacecraft_AODCS",
}

subsystems = {
    "communication": {
        "slug": "COM",
        "ontology": "http://ontology.projectchronos.eussubsystems/Spacecraft_Communication",
        "hasPower": {"min": -200, "max": -1},
        "hasMass": {"min": 30, "max": 100},
        "hasMonetaryValue": {"min": 1000, "max": 10000},
        "minWorkingTemperature": {"min": -40, "max": -20},
        "maxWorkingTemperature": {"min": 40, "max": 90}
    },
    "propulsion": {
        "slug": "PROP",
        "ontology": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Propulsion",
        "hasPower": {"min": -200, "max": -50},
        "hasMass": {"min": 10, "max": 100},
        "hasMonetaryValue": {"min": 5000, "max": 25000},
        "minWorkingTemperature": {"min": -30, "max": -10},
        "maxWorkingTemperature": {"min": 20, "max": 80}
    },
    "detector": {
        "slug": "DTR",
        "ontology": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Detector",
        "hasPower": {"min": -100, "max": -10},
        "hasMass": {"min": 50, "max": 400},
        "hasMonetaryValue": {"min": 2000, "max": 15000},
        "minWorkingTemperature": {"min": -30, "max": -10},
        "maxWorkingTemperature": {"min": 20, "max": 80}
    },
    "primary power": {
        "slug": "PPW",
        "ontology": "http://ontology.projectchronos.eu/subsystems/Spacecraft_PrimaryPower",
        "hasPower": {"min": 200, "max": 2000},
        "density": 1.5,
        "hasMass": {"min": 30, "max": 100},
        "hasMonetaryValue": {"min": 2000, "max": 10000},
        "minWorkingTemperature": {"min": -60, "max": -40},
        "maxWorkingTemperature": {"min": 50, "max": 100}
    },
    "backup power": {
        "slug": "BCK",
        "ontology": "http://ontology.projectchronos.eu/subsystems/Spacecraft_BackupPower",
        "hasPower": {"min": 50, "max": 1500},
        "density": 2,
        "hasMass": {"min": 100, "max": 300},
        "hasMonetaryValue": {"min": 5000, "max": 25000},
        "minWorkingTemperature": {"min": -30, "max": -10},
        "maxWorkingTemperature": {"min": 20, "max": 80}
    },
    "thermal": {
        "slug": "THR",
        "ontology": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Thermal",
        "hasPower": {"min": -100, "max": 100},
        "hasMass": {"min": 20, "max": 150},
        "hasMonetaryValue": {"min": 500, "max": 4000},
        "minTemperature": {"min": -100, "max": -30},
        "maxTemperature": {"min": 50, "max": 100}
    },
    "structure": {
        "slug": "STR",
        "ontology": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Structure",
        "hasMass": {"min": 10, "max": 100},
        "hasMonetaryValue": {"min": 2000, "max": 35000},
        "minWorkingTemperature": {"min": -90, "max": -30},
        "maxWorkingTemperature": {"min": 30, "max": 70}
    },
    "command and data": {
        "slug": "CDH",
        "ontology": "http://ontology.projectchronos.eu/subsystems/Spacecraft_CDH",
        "hasPower": {"min": -50, "max": -5},
        "hasMass": {"min": 20, "max": 70},
        "hasMonetaryValue": {"min": 1000, "max": 5000},
        "minWorkingTemperature": {"min": -20, "max": -10},
        "maxWorkingTemperature": {"min": 10, "max": 50}
    },
    "attitude and orbit control": {
        "slug": "AODCS",
        "ontology": "http://ontology.projectchronos.eu/subsystems/Spacecraft_AODCS",
        "hasPower": {"min": -150, "max": 100},
        "hasMass": {"min": 10, "max": 80},
        "hasMonetaryValue": {"min": 1000, "max": 15000},
        "minWorkingTemperature": {"min": -50, "max": -30},
        "maxWorkingTemperature": {"min": 30, "max": 70},
        "active": ["magnetic torque", "cold gas", "microthrusters"],
        "passive": ["rotation", "gravity", "solar pressure"]
    }
}


def randomValue(interval: Dict[str, int]) -> int:
    """Generate a random integer value from a given interval."""
    if not isinstance(interval, dict):
        raise ValueError('value has to be dict')
    return random.randrange(interval['min'], interval['max'], 1) // 1


def generateObject(name: str, subsystem: Dict[str, Any]) -> Optional[Dict[str, Any]]: # type: ignore
    """Generate random components from given input dictionary."""
    result = {} # type: Dict
    result['hasMass'] = randomValue(subsystem['hasMass'])
    if 'minWorkingTemperature' in subsystem.keys():
        if not name == 'structure':
            result['hasPower'] = randomValue(subsystem['hasPower'])
        result['minWorkingTemperature'] = randomValue(subsystem['minWorkingTemperature'])
        result['maxWorkingTemperature'] = randomValue(subsystem['maxWorkingTemperature'])
        if 'density' in subsystem.keys():  # rule power or battery
            result['hasVolume'] = int(result['hasMass'] / subsystem['density']) // 1
            if name == 'primary power':
                result['hasMonetaryValue'] = result['hasPower'] * 5
                return result
            elif name == 'backup power':
                result['hasMonetaryValue'] = result['hasPower'] * 16
                return result
        else:    # rule for other not generator
            result['hasVolume'] = result['hasMass'] + \
                randomValue({'min': -5, 'max': 5})
            if name not in ['structure', 'attitude and orbit control']:
                if name == 'detector':
                    result['type'] = random.choice(
                        ['interferometer', 'spectrometer', 'photometer', 'optical', 'dust detector'])

                result['hasMonetaryValue'] = randomValue(subsystem['hasMonetaryValue'])
                return result
            else:
                if name == 'structure':
                    result['hasPower'] = 0
                    result['hasMonetaryValue'] = int(350000 / result['hasMass']) // 1
                    return result
                elif name == 'attitude and orbit control':
                    if result['hasPower'] > 0:
                        result['hasPower'] = 0
                        result['type'] = 'passive'
                        result['mechanism'] = random.choice(
                            subsystem['passive'])
                    else:
                        result['type'] = 'active'
                        result['mechanism'] = random.choice(
                            subsystem['active'])
                    result['hasMonetaryValue'] = randomValue(subsystem['hasMonetaryValue'])
                    return result

    else:
        result['hasVolume'] = result['hasMass'] + randomValue({'min': -5, 'max': 5})
        result['hasPower'] = randomValue(subsystem['hasPower'])
        if result['hasPower'] > 0:
            result['hasPower'] = 0
        result['minTemperature'] = randomValue(subsystem['minTemperature'])
        result['maxTemperature'] = randomValue(subsystem['maxTemperature'])

        result['hasMonetaryValue'] = (result['maxTemperature'] - result['minTemperature']) * 20

        if result['hasPower'] == 0:
            result['type'] = 'passive'
        else:
            result['type'] = 'active'
        return result

# def gen_all_types():
#     """Generate one random object for all classes."""
#     output = []
#     global subsystems
#     i = 0
#     for k, v in subsystems.items():
#         # print(k)
#         name = str(random.randrange(0, 50)) + \
#             str(random.choice(['T', 'W', 'KV', 'JFG'])) + ' ' + k
#         obj = {}
#         obj['name'] = name
#         obj['id'] = i + 1
#         obj['object'] = generateObject(k, v)
#         output.append(obj)
#         i += 1
#         break
#     return output
# print(gen_all_types())


# First we will generate data for COTS (spacecraft parts).
# gen_cots will generate n number of spacecraft parts with random properties
def gen_random_object() -> Dict[str, Any]:
    """Generate a random object."""
    index = random.randint(0, len(subsystems.keys())-1)
    k, v = list(subsystems.items())[index]
    name = str(random.randrange(0, 50)) + \
        str(random.choice(['T', 'W', 'KV', 'JFG'])) + ' ' + k
    obj = {} # type: Dict[str, Any]
    obj['name'] = name
    obj['@type'] = classes_keymap[k]
    obj['object'] = generateObject(k, v) #type: ignore
    return obj


def gen_cots(n: int) -> List[Dict[str, Any]]:
    """Generate n number of spacecraft parts with random properties."""
    output = [] # type: List[Dict[str, Any]]
    for num in range(n):
        obj = gen_random_object()
        output.append(obj)
    return output

import json

if __name__ == "__main__":
    print(json.dumps(gen_cots(1), indent=4, sort_keys=True))