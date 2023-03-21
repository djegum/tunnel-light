from phue import Bridge

lights_in_tunnel_1 = 7

class Hue:
    def __init__(self, ip):
        self.bridge = Bridge(ip)
        self.bridge.connect()
        self.auto_mode = {}

        for l in range(1, lights_in_tunnel_1 + 1):
            name = Hue.get_light_name(1, l)
            self.auto_mode[name] = True

    def set_stand_tunnel(self, tunnel, stand):
        for l in range(1, lights_in_tunnel_1 + 1):
            if(self.auto_mode[Hue.get_light_name(tunnel, l)] == 0):
                self.set_stand_light(tunnel, l, stand)

    def set_stand_light(self, tunnel, light, stand):
        name = Hue.get_light_name(tunnel, light)
        if stand == 0:
            self.bridge.set_light(name, 'on', False)
        else:
            self.bridge.set_light(name, 'on', True)
            self.bridge.set_light(name, 'bri', Hue.convert_stand_to_value(stand))

    def get_stand(self, tunnel, light):
        name = Hue.get_light_name(tunnel, light)
        if self.bridge.get_light(name, 'on') == False:
            x = 0
        else:
            x = Hue.convert_value_to_stand(self.bridge.get_light(name, 'bri'))
        return x

    def set_auto(self, tunnel, light, auto):
        self.auto_mode[Hue.get_light_name(tunnel, light)] = auto

    def convert_stand_to_value(stand):
        return int(254 * ( stand / 10 ))

    def convert_value_to_stand(value):
        return int((value / 25))

    def get_light_name(tunnel, light):
        return f"T{tunnel}L{light}"