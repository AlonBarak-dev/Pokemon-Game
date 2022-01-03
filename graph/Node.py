from graph.GeoLocation import GeoLocation


class Node(object):
    """
    This class represent a vertex in a graph.
    """

    def __init__(self, pos: GeoLocation = None, key: int = None):
        """
        a constructor for the Node class.
        :param pos: GeoLocation of the Node.
        :param key: the ID of the Node
        """

        self.key: int = key
        self.pos: GeoLocation = pos
        self.tag: int = 0
        self.edges_in = {}
        self.edges_out = {}
        self.weight: float = 0.0
        self.info: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> 'Node':
        """
        this method creates a Node from a dictionary.
        :param data: Data dict
        :return: Node
        """

        # check for None values and raise exception
        # if 'id' not in data or 'key' not in data:
        #     raise ValueError("Cant create a Node without id and data")
        key: int = data.get('id')  # initialize the node ID

        # initialize the node location
        pos = data.get('pos')
        if pos is not None:
            pos = GeoLocation(*pos.split(','))  # create new GeoLocation

        node: Node = Node(pos, key)

        return node

    def to_dict(self) -> dict:
        """
        this method return a dict representing the Node
        :return: dict with the Node values
        """
        dic = {
            'pos': self.pos.__repr__(),
            'id': self.key
        }
        return dic

    def get_geoLocation(self) -> GeoLocation:
        """
        return the position of the Node
        :return: GeoLocation object
        """
        return self.pos

    def set_geoLocation(self, geo: GeoLocation):
        """
        set the position of the Node to a new position
        :param geo: GeoLocation object
        """
        if not isinstance(geo, GeoLocation):
            raise ValueError("should be GeoLocation type")
        self.pos = geo

    def get_key(self) -> int:
        return self.key

    def get_pos(self) -> GeoLocation:
        return self.pos

    def set_tag(self, tag: int):
        self.tag = tag

    def get_tag(self):
        return self.tag

    def __repr__(self):
        return "{}: |edges out| {} |edges in| {}".format(self.key, len(self.edges_out), len(self.edges_in))
