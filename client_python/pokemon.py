from graph.GeoLocation import GeoLocation
from graph.Node import Node


class Pokemon(Node):

    def __init__(self, value: int, type: int, pos: GeoLocation, key:int):
        super(Pokemon, self).__init__(pos=GeoLocation(pos.x, pos.y, pos.z), key=key)
        self.value = value
        self.type = type
        self.agent_id = None

    @classmethod
    def from_dict_pok(cls, data, key:int) -> 'Pokemon':
        """
        this method creates a Pokemon from a dictionary.
        :param data: Data dict
        :return: Pokemon
        """

        value = int(data.get("value"))  # extract the value of the pokemon from the dict
        type = int(data.get("type"))  # extract the type of the pokemon from the dict
        # initialize the pokemon location
        pos = data.get('pos')
        if pos is not None:
            pos = GeoLocation(*pos.split(','))  # create new GeoLocation

        poki = Pokemon(value, type, pos, key)
        return poki

    # setting some getters for the class
    def get_value(self) -> int:
        return self.value

    def get_type(self) -> int:
        return self.type

    def get_pos(self) -> GeoLocation:
        return self.pos
