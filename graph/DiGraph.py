import math

from client_python.pokemon import Pokemon
from graph.GraphInterface import GraphInterface
from graph.Edge import Edge
from graph.Node import Node
from graph.GeoLocation import GeoLocation


class DiGraph(GraphInterface):

    def __init__(self):
        """
        empty constructor for DiGraph class
        """
        self.mode_count = 0
        self.edges = []
        self.nodes = {}

    def v_size(self) -> int:
        """
        Returns the number of vertices in this graph
        @return: The number of vertices in this graph
        """
        return len(self.nodes)

    def e_size(self) -> int:
        """
        Returns the number of edges in this graph
        @return: The number of edges in this graph
        """

        return len(self.edges)

    def get_all_v(self) -> dict:
        """
        return a dictionary of all the nodes in the Graph, each node is represented using a pair
        (node_id, node_data)
        """
        return self.nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        """
        return a dictionary of all the nodes connected to (into) node_id ,
        each node is represented using a pair (other_node_id, weight)
        """
        output = {}  # new dict
        for edge in self.nodes[id1].edges_in.values():  # iterate over the edges coming into the given node
            output[edge.src] = edge.weight  # (other_node_id, weight)
        return output

    def all_out_edges_of_node(self, id1: int) -> dict:
        """
        return a dictionary of all the nodes connected from node_id , each node is represented using a pair
        (other_node_id, weight)
        """
        output = {}  # new dict
        for edge in self.nodes[id1].edges_out.values():
            output[edge.dest] = edge.weight
        return output

    def get_mc(self) -> int:
        """
        Returns the current version of this graph,
        on every change in the graph state - the MC should be increased
        @return: The current version of this graph.
        """
        return self.mode_count

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        Adds an edge to the graph.
        @param id1: The start node of the edge
        @param id2: The end node of the edge
        @param weight: The weight of the edge
        @return: True if the edge was added successfully, False o.w.
        Note: If the edge already exists or one of the nodes dose not exists the functions will do nothing
        """

        # check whether the given nodes are in the graph or not.
        if id1 not in self.nodes or id2 not in self.nodes:
            return False
        # check whether the given edge already exists in the Graph or not
        for i, edge in enumerate(self.edges):
            if edge.src == id1 and edge.dest == id2:
                return False

        edge = Edge(id1, id2, weight)  # create a new Edge from the given data
        self.edges.append(edge)
        self.nodes[id1].edges_out[id2] = edge
        self.nodes[id2].edges_in[id1] = edge
        self.mode_count += 1  # update mode counter
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
        Adds a node to the graph.
        @param node_id: The node ID
        @param pos: The position of the node
        @return: True if the node was added successfully, False o.w.
        Note: if the node id already exists the node will not be added
        """
        if node_id is None:
            return False
        # check whether the node already exists in the Graph or not
        if node_id in self.nodes:
            return False

        # creates a new Node
        if pos is not None:
            x = pos[0]
            y = pos[1]
            z = pos[2]
            pos = GeoLocation(x, y, z)
            node = Node(pos, node_id)
        else:
            node = Node(key=node_id)
        # adds the new node to the Graph
        self.nodes[node_id] = node
        self.mode_count += 1  # update mode counter
        return True

    def add_pokemon(self, pokemon: Pokemon):
        """
        this method adds a pokemon
        """
        self.nodes[pokemon.key] = pokemon
        self.mode_count += 1

    def find_edge(self, pok: Pokemon) -> tuple:
        res = ()
        for edge in self.edges:
            src_x = self.nodes[edge.src].pos.x
            src_y = self.nodes[edge.src].pos.y
            dest_x = self.nodes[edge.dest].pos.x
            dest_y = self.nodes[edge.dest].pos.y
            pok_x = pok.pos.x
            pok_y = pok.pos.y
            dist_edge = math.sqrt(math.pow(src_x - dest_x, 2) + math.pow(src_y - dest_y, 2))
            dist_src_pok = math.sqrt(math.pow(src_x - pok_x, 2) + math.pow(src_y - pok_y, 2))
            dist_pok_dest = math.sqrt(math.pow(dest_x - pok_x, 2) + math.pow(dest_y - pok_y, 2))
            if dist_edge + 0.0001 >= dist_pok_dest + dist_src_pok:
                if (edge.src > edge.dest and pok.type > 0) or (edge.src < edge.dest and pok.type < 0):
                    weight1 = edge.weight * (dist_src_pok / dist_edge)
                    weight2 = edge.weight - weight1
                    return edge, weight1, weight2
        return res

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        Removes an edge from the graph.
        @param node_id1: The start node of the edge
        @param node_id2: The end node of the edge
        @return: True if the edge was removed successfully, False o.w.
        Note: If such an edge does not exists the function will do nothing
        """

        # check whether the given nodes exists in the Graph or not
        if node_id1 not in self.nodes or node_id2 not in self.nodes:
            return False
        # check whether the given edge exists in the graph or not
        x = False
        for i, edge in enumerate(self.edges):
            if edge.src == node_id1 and edge.dest == node_id2:
                self.edges.remove(self.edges[i])
                x = True
                break
        if x:
            # removes all the edges that getting out of the node
            del self.nodes[node_id1].edges_out[node_id2]
            # removes all the edges that getting into the node
            del self.nodes[node_id2].edges_in[node_id1]
            self.mode_count += 1  # update mode counter
            return x
        else:
            return x

    def remove_node(self, node_id: int) -> bool:
        """
       Removes a node from the graph.
       @param node_id: The node ID
       @return: True if the node was removed successfully, False o.w.
       Note: if the node id does not exists the function will do nothing
       """
        # checks whether the particular node exists or not
        if node_id not in self.nodes:
            return False

        for node in self.nodes.values():
            # removes all the edges that getting into the node
            if node_id in node.edges_in:
                del node.edges_in[node_id]
            # removes all the edges that getting out of the node
            if node_id in node.edges_out:
                del node.edges_out[node_id]
        # remove all edges coming in/out of the given node
        remove_list = []
        for edge in self.edges:
            if edge.src == node_id or edge.dest == node_id:
                remove_list.append(edge)
        for edge in remove_list:
            self.edges.remove(edge)

        # deletes the particular node from the Graph
        del self.nodes[node_id]

        self.mode_count += 1  # update mode counter

        return True

    def add_node2(self, other: Node):
        """
        add a Node to the graph.
        :param other: the Node which will be added to the Graph
        :return: True if possible, False if not
        """
        if other.get_pos() is not None:
            return self.add_node(other.get_key(), other.get_pos().to_tuple())
        return self.add_node(other.get_key())

    def add_edge2(self, other: Edge):
        """
       add an Edge to the graph.
       :param other: the Edge which will be added to the Graph
       :return: True if possible, False if not
       """
        return self.add_edge(other.src, other.dest, other.weight)

    def __repr__(self):
        return "Graph: |V|={} , |E|={}".format(self.v_size(), self.e_size())

    def to_dict(self) -> dict:
        """
        this method return a dict representing the graph
        """

        # define the struct of the dict
        dict_res = {'Edges': [],
                    'Nodes': []}
        # loop every node and add its dict to dict_res
        for node in self.nodes.values():
            node_dict = node.to_dict()
            dict_res['Nodes'].append(node_dict)
        # loop every edge and add its dict to dict_res
        for edge in self.edges:
            edge_dict = edge.to_dict()
            dict_res['Edges'].append(edge_dict)

        return dict_res
