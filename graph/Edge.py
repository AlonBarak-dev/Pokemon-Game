class Edge(object):

    def __init__(self, src: int, dest: int, weight: float, info: str = "", tag: int = 0):
        """
        a constructor that create a new instance of Edge.
        :param src: graph ID
        :param dest: dest ID
        :param weight: weight of the Edge
        :param info: represent the data of the Edge
        :param tag: an Integer
        """
        self.src: int = src
        self.dest: int = dest
        self.weight = weight
        self.info = info
        self.tag = tag

    @classmethod
    def from_dict(cls, data: dict):
        """
        create a new instance of Edge from a dict containing all the parameters needed to create
        a new Edge.
        """
        if 'src' not in data or 'dest' not in data:
            raise ValueError("missing values")

        src = int(data.get('src'))
        dest = int(data.get('dest'))
        weight = float(data.get('w'))

        return cls(src=src, dest=dest, weight=weight)

    def to_dict(self) -> dict:
        """
        return a dict from the values of the Edge.
        """
        return {
            'src': self.src,
            'w': self.weight,
            'dest': self.dest
        }


    def __repr__(self):
        return "src: {}, dest: {}, weight: {}"