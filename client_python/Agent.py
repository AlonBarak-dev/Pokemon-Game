from graph.GeoLocation import GeoLocation


class Agent(object):

    def __init__(self, id: int, value: int, src: int, dest: int, speed: float, pos: GeoLocation):
        """
        a constructor for the Agent Class
        """
        self.id = id
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        self.pos = GeoLocation(pos.x, pos.y, pos.z)
        self.path = []

    @classmethod
    def from_dict(self, data: dict) -> 'Agent':
        """
        this method creates an agent from a dict
        """
        id = int(data.get("id"))
        value = int(data.get("value"))
        src = int(data.get("src"))
        dest = int(data.get("dest"))
        speed = float(data.get("speed"))

        # initialize the agent location
        pos = data.get('pos')
        if pos is not None:
            pos = GeoLocation(*pos.split(','))  # create new GeoLocation

        agent = Agent(id, value, src, dest, speed, pos)
        return agent

    def get_id(self):
        return self.id

    def get_value(self):
        return self.value

    def get_src(self):
        return self.src

    def set_src(self, src: int):
        self.src = src

    def set_dest(self, dest: int):
        self.dest = dest

    def get_dest(self):
        return self.dest

    def get_speed(self):
        return self.speed

    def set_speed(self, speed: int):
        self.speed = speed

    def get_pos(self) -> GeoLocation:
        return self.pos
