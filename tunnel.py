from pyModbusTCP.server import ModbusServer
from hue import Hue
import config

# Create instance of ModbusServer, with no block set to true
# the server doesn't block the program from executing further
server = ModbusServer(config.ipPi, 502, no_block=True)

# Get Hue bridge at the right ip address

setRegisters1 = {
    '1': {
        'setStand':{
            'old': None,
            'reg': 43000
        },
        'setAuto':{
            'old': None,
            'reg': 43001
        }
    },
    '2': {
        'setStand':{
            'old': None,
            'reg': 43006
        },
        'setAuto':{
            'old': None,
            'reg': 43007
        }
    },
    '3': {
        'setStand':{
            'old': None,
            'reg': 43012
        },
        'setAuto':{
            'old': None,
            'reg': 43013
        }
    },
    '4': {
        'setStand':{
            'old': None,
            'reg': 43018
        },
        'setAuto':{
            'old': None,
            'reg': 43019
        }
    },
    '5': {
        'setStand':{
            'old': None,
            'reg': 43024
        },
        'setAuto':{
            'old': None,
            'reg': 43025
        }
    },
    '6': {
        'setStand':{
            'old': None,
            'reg': 43030
        },
        'setAuto':{
            'old': None,
            'reg': 43031
        }
    },
    '7': {
        'setStand':{
            'old': None,
            'reg': 43036
        },
        'setAuto':{
            'old': None,
            'reg': 43037
        }
    }
}

getRegisters1 = {
    '1':{
        'Niveau': {
            'addr': 43002,
            'old': None
        },
    },
    '2':{
        'Niveau': {
            'addr': 43008,
            'old': None
        },
    },
    '3':{
        'Niveau': {
            'addr': 43014,
            'old': None
        },
    },
    '4':{
        'Niveau': {
            'addr': 43020,
            'old': None
        },
    },
    '5':{
        'Niveau': {
            'addr': 43026,
            'old': None
        },
    },
    '6':{
        'Niveau': {
            'addr': 43032,
            'old': None
        },
    },
    '7':{
        'Niveau': {
            'addr': 43038,
            'old': None
        },
    }
}

setRegisters2 = {
    '1': {
        'setStand':{
            'old': None,
            'reg': 45000
        },
        'setAuto':{
            'old': None,
            'reg': 45001
        }
    },
    '2': {
        'setStand':{
            'old': None,
            'reg': 45006
        },
        'setAuto':{
            'old': None,
            'reg': 45007
        }
    },
    '3': {
        'setStand':{
            'old': None,
            'reg': 45012
        },
        'setAuto':{
            'old': None,
            'reg': 45013
        }
    },
    '4': {
        'setStand':{
            'old': None,
            'reg': 45018
        },
        'setAuto':{
            'old': None,
            'reg': 45019
        }
    },
    '5': {
        'setStand':{
            'old': None,
            'reg': 45024
        },
        'setAuto':{
            'old': None,
            'reg': 45025
        }
    },
    '6': {
        'setStand':{
            'old': None,
            'reg': 45030
        },
        'setAuto':{
            'old': None,
            'reg': 45031
        }
    },
    '7': {
        'setStand':{
            'old': None,
            'reg': 45036
        },
        'setAuto':{
            'old': None,
            'reg': 45037
        }
    }
}

getRegisters2 = {
    '1':{
        'Niveau': {
            'addr': 45002,
            'old': None
        },
    },
    '2':{
        'Niveau': {
            'addr': 45008,
            'old': None
        },
    },
    '3':{
        'Niveau': {
            'addr': 45014,
            'old': None
        },
    },
    '4':{
        'Niveau': {
            'addr': 45020,
            'old': None
        },
    },
    '5':{
        'Niveau': {
            'addr': 45026,
            'old': None
        },
    },
    '6':{
        'Niveau': {
            'addr': 45032,
            'old': None
        },
    },
    '7':{
        'Niveau': {
            'addr': 45038,
            'old': None
        },
    }
}

try:
    print("Starting Modbus server and connecting to Hue bridge...")
    server.start()
    print("Modbus server online.")
    hue = Hue(config.ipHue)
    print("Connected to Hue bridge")

    groupSetStandOld1 = None
    groupSetStandOld2 = None

    while True:

        for device, value in setRegisters1.items():
            for key, value in value.items():
                current = server.data_bank.get_holding_registers(value['reg'], 1)
                if value['old'] != current:
                    print(f"T1 Value of {device}:{key} changed to {current}")
                    value['old'] = current
                    if key == 'setStand':
                        hue.set_stand_light(1, device, current[0])
                    elif key == 'setAuto':
                        hue.set_auto(1, device, current[0])

        groupSetStand = server.data_bank.get_holding_registers(42000, 1)
        if groupSetStand != groupSetStandOld1:
            print("T1 Value of groupSetStand changed to: ", groupSetStand)
            hue.set_stand_tunnel(1, groupSetStand[0])
            groupSetStandOld1 = groupSetStand

        for device, values in getRegisters1.items():
            for value, properties in values.items():
                if value == 'Niveau':
                    x = hue.get_stand(1, device)
                    if x != properties['old']:
                        print(f"T1 Setting {device}:{value} to {x}")
                        server.data_bank.set_holding_registers(properties['addr'], [x])
                        properties['old'] = x;

        for device, value in setRegisters2.items():
            for key, value in value.items():
                current = server.data_bank.get_holding_registers(value['reg'], 1)
                if value['old'] != current:
                    print(f"Value of {device}:{key} changed to {current}")
                    value['old'] = current
                    if key == 'setStand':
                        hue.set_stand_light(2, device, current[0])
                    elif key == 'setAuto':
                        hue.set_auto(2, device, current[0])

        groupSetStand = server.data_bank.get_holding_registers(44000, 1)
        if groupSetStand != groupSetStandOld2:
            print("T2: Value of groupSetStand changed to: ", groupSetStand)
            hue.set_stand_tunnel(2, groupSetStand[0])
            groupSetStandOld2 = groupSetStand

        for device, values in getRegisters2.items():
            for value, properties in values.items():
                if value == 'Niveau':
                    x = hue.get_stand(2, device)
                    if x != properties['old']:
                        print(f"T2: Setting {device}:{value} to {x}")
                        server.data_bank.set_holding_registers(properties['addr'], [x])
                        properties['old'] = x;

except KeyboardInterrupt:
    print("Shutting down Modbus server...")
    server.stop()
    print("Modbus server offline.")
except Exception as e:
    print(e)
    print("Shutting down Modbus server...")
    server.stop()
    print("Modbus server offline.")