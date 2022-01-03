import unittest
from graph.GeoLocation import GeoLocation
from graph.Node import Node
from graph.Edge import Edge
from graph.DiGraph import DiGraph


class TestDiGraph(unittest.TestCase):
    # init graph
    graph = DiGraph()
    # init GeoLocation
    p1 = GeoLocation(0.0, 0.0, 0.0)
    # init Nodes
    node0 = Node(p1, 0)
    node1 = Node(key=1)  # no position
    node2 = Node(p1, 2)
    node3 = Node(p1, 3)
    node4 = Node(key=4)  # no position
    # init Edges
    edge01 = Edge(0, 1, 5.0)
    edge04 = Edge(0, 4, 4.2)
    edge23 = Edge(2, 3, 8)
    edge31 = Edge(3, 1, 0.5)
    edge24 = Edge(2, 4, 1)

    def build_graph(self):
        """
        create a basic graph every call.
        used in the tests below.
        """
        self.graph.add_node2(self.node0)
        self.graph.add_node2(self.node1)
        self.graph.add_node2(self.node2)
        self.graph.add_node2(self.node3)
        self.graph.add_node2(self.node4)
        self.graph.add_edge2(self.edge01)
        self.graph.add_edge2(self.edge04)
        self.graph.add_edge2(self.edge23)
        self.graph.add_edge2(self.edge31)
        self.graph.add_edge2(self.edge24)

    def reset_graph(self):
        """
        reset the graph every call.
        used in the tests below.
        """
        self.graph.remove_node(0)
        self.graph.remove_node(1)
        self.graph.remove_node(2)
        self.graph.remove_node(3)
        self.graph.remove_node(4)
        self.graph.mode_count = 0

    def test_v_size(self):
        self.reset_graph()
        self.build_graph()
        size = self.graph.v_size()
        assert size == 5, "wrong vertex size"
        self.graph.remove_node(0)
        size = self.graph.v_size()
        assert size == 4, "should've changed to 4"

    def test_e_size(self):
        self.reset_graph()
        self.build_graph()
        size = self.graph.e_size()
        assert size == 5, "wrong edges size"
        self.graph.remove_edge(0, 1)
        size = self.graph.e_size()
        assert size == 4, "should've been 4 edges left after delete"

    def test_get_all_v(self):
        self.reset_graph()
        self.build_graph()
        allV = self.graph.get_all_v()
        size = self.graph.v_size()
        assert size == len(allV), "wrong vertex size"
        for k, v in allV.items():
            assert v.key == k

    def test_all_in_edges_of_node(self):
        self.reset_graph()
        self.build_graph()
        self.graph.add_edge(1, 4, 0)
        self.graph.add_edge(3, 4, 0)
        in_edges = self.graph.all_in_edges_of_node(4)
        assert len(in_edges) == 4, "wrong number of in edges"
        for i in [0, 1, 2, 3]:
            assert i in in_edges.keys(), "4th node have edges from any other node in the graph!"

    def test_all_out_edges_of_node(self):
        self.reset_graph()
        self.build_graph()
        self.graph.add_edge(0, 2, 0)
        self.graph.add_edge(0, 3, 0)
        out_edges = self.graph.all_out_edges_of_node(0)
        assert len(out_edges) == 4, "wrong number of out edges"
        for i in [1, 2, 3, 4]:
            assert i in out_edges.keys(), "0th node have edges to any other node in the graph!"

    def test_get_mc(self):
        self.reset_graph()
        self.build_graph()
        mc = self.graph.get_mc()
        assert mc == 10, "10 changes happens in build_graph() method"

    def test_add_node(self):
        self.reset_graph()
        assert self.graph.v_size() == 0, "No vertexes in graph"
        assert self.graph.add_node(node_id=0) is True, "no duplicates"
        assert self.graph.add_node(node_id=1) is True, "no duplicates"
        assert self.graph.add_node(node_id=2) is True, "no duplicates"
        assert self.graph.add_node(node_id=3) is True, "no duplicates"
        assert self.graph.add_node(node_id=4) is True, "no duplicates"
        assert self.graph.v_size() == 5, "five vertexes in graph"
        assert self.graph.add_node(node_id=0) is False, "duplicates"
        assert self.graph.v_size() == 5, "still five vertexes in graph"

    def test_add_edge(self):
        self.reset_graph()
        self.graph.add_node2(self.node0)
        self.graph.add_node2(self.node1)
        self.graph.add_node2(self.node2)
        self.graph.add_node2(self.node3)
        self.graph.add_node2(self.node4)
        size = self.graph.e_size()
        assert size == 0, "no edges in graph"
        assert self.graph.add_edge(0,1,5.78) is True, "no duplicates"
        assert self.graph.add_edge(0,2,0.78) is True, "no duplicates"
        assert self.graph.add_edge(1,4,3.78) is True, "no duplicates"
        assert self.graph.add_edge(3,2,2.78) is True, "no duplicates"
        assert self.graph.add_edge(4,0,4.78) is True, "no duplicates"
        size = self.graph.e_size()
        assert size == 5, "five edges in graph"
        assert self.graph.add_edge(4,0,4.78) is False, "duplicates"
        assert self.graph.add_edge(4,0,0.0) is False, "duplicates"
        size = self.graph.e_size()
        assert size == 5, "still five edges in graph"

    def test_remove_edge(self):
        self.reset_graph()
        self.build_graph()
        size = self.graph.e_size()
        assert size == 5, "five edges in graph"
        self.graph.remove_edge(0, 1)
        size = self.graph.e_size()
        assert size == 4, "four edges in graph after delete"
        self.graph.remove_edge(0, 1)        # try to delete (0,1) again
        size = self.graph.e_size()
        assert size == 4, "still four edges in graph after delete"

    def test_remove_node(self):
        self.reset_graph()
        self.build_graph()
        size_v = self.graph.v_size()
        size_e = self.graph.e_size()
        assert size_e == 5, "five edges in graph"
        assert size_v == 5, "five nodes in graph"
        self.graph.remove_node(0)       # removing the 0th node
        size_v = self.graph.v_size()
        size_e = self.graph.e_size()
        assert size_e == 3, "3 edges in graph"
        assert size_v == 4, "4 nodes in graph"

if __name__ == '__main__':
    unittest.main()