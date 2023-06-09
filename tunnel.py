from pyModbusTCP.server import ModbusServer
from hue import Hue

# Create instance of ModbusServer, with no block set to true
# the server doesn't block the program from executing further
server = ModbusServer("127.0.0.1", 502, no_block=True)

# Get Hue bridge at the right ip address

setRegisters = {
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

getRegisters = {
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

try:
    print("Starting Modbus server and connecting to Hue bridge...")
    server.start()
    print("Modbus server online.")
    hue = Hue("192.168.69.100")
    print("Connected to Hue bridge")

    groupSetStandOld = None

    while True:

        for device, value in setRegisters.items():
            for key, value in value.items():
                current = server.data_bank.get_holding_registers(value['reg'], 1)
                if value['old'] != current:
                    print(f"Value of {device}:{key} changed to {current}")
                    value['old'] = current
                    if key == 'setStand':
                        hue.set_stand_light(1, device, current[0])
                    elif key == 'setAuto':
                        hue.set_auto(1, device, current[0])

        groupSetStand = server.data_bank.get_holding_registers(42000, 1)
        if groupSetStand != groupSetStandOld:
            print("Value of groupSetStand changed to: ", groupSetStand)
            hue.set_stand_tunnel(1, groupSetStand[0])
            groupSetStandOld = groupSetStand

        for device, values in getRegisters.items():
            for value, properties in values.items():
                if value == 'Niveau':
                    x = hue.get_stand(1, device)
                    if x != properties['old']:
                        print(f"Setting {device}:{value} to {x}")
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