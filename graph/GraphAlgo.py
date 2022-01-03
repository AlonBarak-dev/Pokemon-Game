import math
import random
import traceback
from _heapq import heappop
from abc import ABC
from heapq import heappush
from typing import List, Dict
from graph import GraphInterface
from graph.GraphAlgoInterface import GraphAlgoInterface
from graph.Edge import Edge
from graph.Node import Node
from graph.GeoLocation import GeoLocation
from graph.DiGraph import DiGraph
import json
import matplotlib.pyplot as plt


class GraphAlgo(GraphAlgoInterface):
    """
    This class implement the abstract class GraphAlgoInterface from graph Directory.
    It allows the User to run different algorithms on the Graph
    """

    def __init__(self, g: DiGraph = None):
        if g is not None:
            self.graph = g
        else:
            self.graph: DiGraph = DiGraph()

    def get_graph(self) -> GraphInterface:
        return self.graph

    def load_from_json(self, data) -> bool:
        """
        Loads a graph from a json file.
        @param data: The path to the json file
        @returns True if the loading was successful, False o.w.
        """
        self.graph = DiGraph()

        nodes = data.get("Nodes")  # the nodes dict
        edges = data.get("Edges")  # the edges dict

        for node in nodes:
            new_node: Node = Node.from_dict(node)  # creating new nodes from the dict
            self.graph.add_node2(new_node)  # adding to the graph

        for edge in edges:
            new_edge: Edge = Edge.from_dict(edge)  # creating new edges from the dict
            self.graph.add_edge2(new_edge)  # adding the edges to the graph

        return True



    def save_to_json(self, file_name: str) -> bool:
        """
        Saves the graph in JSON format to a file
        @param file_name: The path to the out file
        @return: True if the save was successful, False o.w.
        """
        try:
            with open(file_name, 'w+') as file:
                file.write(json.dumps(self.graph.to_dict()))
            return True
        except:
            traceback.print_exc()
            return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, a list of the nodes ids that the path goes through
        """
        self.reset_tags()  # reset all tags to 0 -> NOT VISITED

        source = id1
        destination = id2
        deltas: Dict[int, float] = {}  # represent the 2D array of distances in dijkstra algorithm
        priority_q: [] = []  # a list representing the priority Queue we used in EX2

        total_dist = float(('inf'))  # init the return dist
        path = []

        # in case one of the nodes is not in the graph
        if id1 not in self.graph.nodes or id2 not in self.graph.nodes:
            result = (float(('inf')), path)  # default tuple
            return result

        heappush(priority_q, (0.0, self.get_graph().get_all_v().get(source)))
        deltas[source] = 0.0

        dest_node: Node = None

        while len(priority_q) > 0:

            node_distance, node = heappop(priority_q)  # Extract node with minimum delta(dist) and its delta

            node.tag = 1
            if node.key == destination:
                dest_node = node

            # iterate over the neighbors of node (out edges)
            for ngbr_id, ngbr_w in self.get_graph().all_out_edges_of_node(node.key).items():

                neighbour: Node = self.get_graph().get_all_v().get(ngbr_id)  # neighbor node

                if neighbour.tag == 1:  # if the node already visited, skip him
                    continue

                new_neighbour_delta = deltas.get(node.key) + ngbr_w  # calculating the new delta
                self.relax(new_neighbour_delta, deltas, neighbour, priority_q, ngbr_id, node)  # relax the map

        if dest_node is not None:  # Reached the desired Node (there is a path)
            total_dist = deltas.get(destination)
            path = self.__backtrack_path(source, dest_node)

        # Reset tags back to 0 when finished
        self.reset_tags()

        result = (total_dist, path)  # the result tuple with its new data (the total distance of the path, the path)
        return result

    def relax(self, new_neighbour_delta: float, deltas: Dict[int, float], neighbour: Node, priority_q: list,
              ngbr_id: int, node: Node):
        if new_neighbour_delta < deltas.get(ngbr_id, float("inf")):
            heappush(priority_q, (new_neighbour_delta, neighbour))
            deltas[ngbr_id] = new_neighbour_delta
            neighbour.tag = 2  # node is queued
            neighbour.info = "{}".format(node.key)  # update the info so it contain its parent key so we
            # can track the path after we done

    def __backtrack_path(self, src: int, dest_node: Node) -> List[Node]:
        """
        create a path for shortest path.
        :param src: source Node.
        :param dest_node: Destination Node.
        :return: list of nodes
        """
        path: List = []  # A list which will contain the nodes in the shortest path

        child: Node = dest_node  # the last child in our path

        while child.key != src:  # DO SO until first parent is reached(graph node)

            path.insert(0, child.key)
            if child.info:  # has parent?
                child = self.get_graph().get_all_v().get(int(child.info))  # update child to its father

        path.insert(0, child.key)  # insert the graph node as well

        return path

    def reset_tags(self):
        """
        This method reset all the graph's Node's tags to 0 -> NOT VISITED YET
        """
        for n in self.get_graph().get_all_v().values():
            n.tag = 0  # NOT VISITED YET

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        """
        Finds the shortest path that visits all the nodes in the list
        :param node_lst: A list of nodes id's
        :return: A list of the nodes id's in the path, and the overall distance
        """

        path: list = []  # the returned path
        total_dist = 0
        visited: list = []
        # set all tags to unvisited(0)
        self.reset_tags()

        v = node_lst[0]  # start Node
        path.append(v)
        self.get_graph().nodes[v].tag = 1  # mark as visited
        visited.append(v)
        # loop until all wanted nodes are visited
        while len(visited) < len(node_lst):

            u, dist, path_vu = self.min_shortest_path(v, node_lst)  # return the closest node to v
            # if u in visited:
            #     return ([], float(('inf')))
            total_dist += dist
            for n in path_vu:
                if n == path[len(path) - 1]:
                    continue
                if n in node_lst:
                    self.graph.nodes[n].set_tag(1)  # mark as visited
                    if n not in visited:  # add to visited list
                        visited.append(n)
                path.append(n)

            v = u  # move to the next node

        return path, total_dist

    def min_shortest_path(self, key: int, node_lst: List[int]) -> (int, float, List[int]):
        """
        This method return the nearest node to key as well as the distance between them
        and the path from key to the nearest node.
        :param key: the id of the source node
        :param node_lst: list of nodes should be "visited"
        :return int: the nearest node's ID
        :return float: the distance from key to the nearest node
        :return List[int]: the path from key to its nearest node
        """

        min_dist = 99999
        dest_node = key
        final_path: List[int] = []
        # loop over the unvisited nodes in node_lst
        for i in node_lst:
            if self.graph.nodes[i].get_tag() == 0 and self.graph.nodes[i].key != key:
                # remember the nodes who were already visited
                visited = []
                for node in self.graph.nodes.values():
                    if node.tag == 1:
                        visited.append(node.key)

                dist, path = self.shortest_path(key, i)  # find the shortest path from key to i

                # remember the nodes who were already visited
                for node in visited:
                    self.graph.nodes[node].set_tag(1)

                    # in case we found a closer node, update
                if dist < min_dist:
                    min_dist = dist
                    final_path = path
                    dest_node = i

        return dest_node, min_dist, final_path

    def centerPoint(self) -> (int, float):
        """
        Finds the node that has the shortest distance to it's farthest node,
        assuming the graph is strongly connected.
        :return: The nodes id, min-maximum distance
        """
        min_max_sp = 999999  # the minimum from the maximum shortest paths
        chosen_node = -1  # ID of the center

        for node in self.graph.get_all_v().values():

            max_sp = self.max_shortest_path(node.key)
            if max_sp < min_max_sp:
                min_max_sp = max_sp
                chosen_node = node.key

        return chosen_node, min_max_sp

    def max_shortest_path(self, key) -> float:
        """
        This method finds the shortest paths from given node to all other
        nodes in the graph using dijkstra algorithm.
        the method return the maximum shortest path it finds.
        """
        self.reset_tags()  # reset all tags to 0 -> NOT VISITED

        source = key
        deltas: Dict[int, float] = {}  # represent the 2D array of distances in dijkstra algorithm
        priority_q: [] = []  # a list representing the priority Queue we used in EX2

        total_dist = -1  # init the return dist
        path = []

        # in case one of the nodes is not in the graph
        if source not in self.graph.nodes:
            return 99999

        heappush(priority_q, (0.0, self.get_graph().get_all_v().get(source)))
        deltas[source] = 0.0

        while len(priority_q) > 0:

            node_distance, node = heappop(priority_q)  # Extract node with minimum delta(dist) and its delta

            node.tag = 1

            # iterate over the neighbors of node (out edges)
            for ngbr_id, ngbr_w in self.get_graph().all_out_edges_of_node(node.key).items():

                neighbour: Node = self.get_graph().get_all_v().get(ngbr_id)  # neighbor node

                if neighbour.tag == 1:  # if the node already visited, skip him
                    continue

                new_neighbour_delta = deltas.get(node.key) + ngbr_w  # calculating the new delta
                self.relax(new_neighbour_delta, deltas, neighbour, priority_q, ngbr_id, node)  # relax the map

        # Reset tags back to 0 when finished
        self.reset_tags()
        # find the maximum path from node to any node
        max_sp = -1
        for w in deltas.values():
            if w > max_sp:
                max_sp = w

        return max_sp

    def generate_pos(self, node: Node):
        """
        this method generate position for a node base on its distance from the Center node
        in the graph.
        :param node: the position less node
        """
        center_id, dist = self.centerPoint()        # finds the center in the graph

        if self.graph.nodes[center_id].pos is None:     # if center also dont have position, generate constant position
            self.graph.nodes[center_id].pos = GeoLocation(1.0, 1.5, 0.0)

        center_node = self.graph.nodes[center_id]       # the center node
        # extract the center position (x,y)
        center_x = center_node.pos.x
        center_y = center_node.pos.y
        # generate x,y values for the given node
        theta = random.uniform(0, 2 * math.pi)      # random angle theta
        # radius = random.gauss(1.0, 0.1)
        radius, path = self.shortest_path(node.key, center_id)      # radius = distance from center
        # x and y
        x = center_x + radius * math.cos(theta)
        y = center_y + radius * math.sin(theta)
        # create a new position for the node
        node.pos = GeoLocation(x, y, 0.0)

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """

        # define the Xs and Ys lists who will be used for scattering
        xs = []
        ys = []

        nodes = self.get_graph().get_all_v()        # the graph's nodes

        # loop every node in the graph
        for n in nodes.values():
            # if it has no position -> generate a random one
            if not n.pos:
                self.generate_pos(n)

            # add the node position in the lists
            xs.append(n.pos.x)
            ys.append(n.pos.y)
            # node attributes
            plt.text(n.pos.x, n.pos.y, n.key,
                     va='top',
                     ha='right',
                     color='red',
                     fontsize=9,
                     bbox=dict(boxstyle='square, pad=0.2', ec='gray', fc='pink', alpha=0.65),
                     zorder=99)

            # lop every out_edge of the specific node
            for node_id in self.get_graph().all_out_edges_of_node(n.key):
                node_c = nodes.get(node_id)     # a neighbour of node

                # if neighbour dont have position, generate one
                if not node_c.pos:
                    self.generate_pos(node_c)

                x = n.pos.x
                y = n.pos.y
                # edge attributes
                plt.annotate("",
                             xy=(node_c.pos.x, node_c.pos.y),
                             xycoords='data',
                             xytext=(x, y),
                             textcoords='data',
                             arrowprops=dict(arrowstyle="->", color='black',
                                             connectionstyle="arc3,rad={}".format(0.15)),
                             )

        # print the nodes and the edges
        plt.scatter(xs, ys, color='blue')
        plt.draw()
        plt.show()
