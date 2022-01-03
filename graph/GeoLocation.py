from math import sqrt


class GeoLocation(object):
    '''
    represent a x,y,z point in space
    '''

    def __init__(self, x: float, y: float, z: float):
        self.x: float = float(x)
        self.y: float = float(y)
        self.z: float = float(z)



    def __repr__(self) -> str:
        return "{},{},{}".format(self.x, self.y, self.z)

    def distance(self, geo: 'GeoLocation') -> float:
        '''
        return distance between two points.
        :param geo: a GeoLocation instance.
        :return: distance from self to geo.
        '''
        dx = self.x - geo.x
        dy = self.y - geo.y
        dz = self.z - geo.z
        dist = sqrt(dx*dx + dy*dy + dz*dz)
        return dist

    def to_tuple(self) -> tuple:
        ret = [self.x, self.y, self.z]
        return tuple(ret)



