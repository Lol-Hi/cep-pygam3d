import math

def newgety(coords, constants):
    gradient = constants.screenheight / constants.cameradistance
    return 1.0 * coords.y / coords.z / gradient * constants.screenheight

def newgetx(coords, constants):
    # must take into account position of player
    theta = math.degrees(math.atan(1.0 * coords.x / coords.z)) + constants.fov / 2
    return 1.0 * theta / constants.fov * constants.screenwidth

class Coords:
    x = 1.5
    y = 5
    z = 5
    def set(self, tup):
        self.x = tup[0]
        self.y = tup[1]
        self.z = tup[2]

class Data:
    screenheight = 500
    screenwidth = 400
    fov = 120
    cameradistance = 300


constants = Data()
coords = Coords()

#print(newgetx(coords, constants))
#print(newgety(coords, constants))
