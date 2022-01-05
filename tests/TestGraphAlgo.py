import json

from graph import DiGraph, GraphInterface
from graph.GraphAlgo import GraphAlgo
import unittest


class TestGraphAlgo(unittest.TestCase):
    file_name = '{"Edges":[{"src":0,"w":1.4004465106761335,"dest":1},{"src":0,"w":1.4620268165085584,"dest":10},' \
                '{"src":1,"w":1.8884659521433524,"dest":0},{"src":1,"w":1.7646903245689283,"dest":2},{"src":2,' \
                '"w":1.7155926739282625,"dest":1},{"src":2,"w":1.1435447583365383,"dest":3},{"src":3,' \
                '"w":1.0980094622804095,"dest":2},{"src":3,"w":1.4301580756736283,"dest":4},{"src":4,' \
                '"w":1.4899867265011255,"dest":3},{"src":4,"w":1.9442789961315767,"dest":5},{"src":5,' \
                '"w":1.4622464066335845,"dest":4},{"src":5,"w":1.160662656360925,"dest":6},{"src":6,' \
                '"w":1.6677173820549975,"dest":5},{"src":6,"w":1.3968360163668776,"dest":7},{"src":7,' \
                '"w":1.0176531013725074,"dest":6},{"src":7,"w":1.354895648936991,"dest":8},{"src":8,' \
                '"w":1.6449953452844968,"dest":7},{"src":8,"w":1.8526880332753517,"dest":9},{"src":9,' \
                '"w":1.4575484853801393,"dest":8},{"src":9,"w":1.022651770039933,"dest":10},{"src":10,' \
                '"w":1.1761238717867548,"dest":0},{"src":10,"w":1.0887225789883779,"dest":9}],"Nodes":[{' \
                '"pos":"35.18753053591606,32.10378225882353,0.0","id":0},{"pos":"35.18958953510896,32.10785303529412,' \
                '0.0","id":1},{"pos":"35.19341035835351,32.10610841680672,0.0","id":2},{"pos":"35.197528356739305,' \
                '32.1053088,0.0","id":3},{"pos":"35.2016888087167,32.10601755126051,0.0","id":4},' \
                '{"pos":"35.20582803389831,32.10625380168067,0.0","id":5},{"pos":"35.20792948668281,' \
                '32.10470908739496,0.0","id":6},{"pos":"35.20746249717514,32.10254648739496,0.0","id":7},' \
                '{"pos":"35.20319591121872,32.1031462,0.0","id":8},{"pos":"35.19597880064568,32.10154696638656,0.0",' \
                '"id":9},{"pos":"35.18910131880549,32.103618700840336,0.0","id":10}]} '
    json_object = json.loads(file_name)

    def test_load_from_json(self):
        graph_algo = GraphAlgo()
        assert graph_algo.load_from_json(self.json_object) is True, "load from json failed"
        assert graph_algo.get_graph().v_size() == 11, "load wasn't full"
        assert graph_algo.get_graph().e_size() == 22, "load wasn't full"
        """
        the below tests were used to determine the runTime for graphs with 1000 and 10000 nodes.
        no need to run them -> needed files are not included.
        """
        # assert graph_algo.load_from_json("../../data/1000Nodes.json") is True, "1000 nodes went wrong"
        # assert graph_algo.load_from_json("../../data/10000Nodes.json") is True, "10000 nodes went wrong"

    # def test_save_to_json(self):
    #     graph_algo = GraphAlgo()
    #     assert graph_algo.load_from_json(self.json_object) is True, "load from json failed"
    #     assert graph_algo.save_to_json("../../data/output0.json") is True, "The save process failed"
    #     graph_algo.load_from_json("../../data/output0.json")
    #     assert graph_algo.get_graph().v_size() == 11, "save wasn't full"
    #     assert graph_algo.get_graph().e_size() == 22, "save wasn't full"
    #     """
    #     the below tests were used to determine the runTime for graphs with 1000 and 10000 nodes.
    #     no need to run them -> needed files are not included.
    #     """
    #     # assert graph_algo.load_from_json("../../data/1000Nodes.json") is True, "1000 nodes went wrong"
    #     # assert graph_algo.save_to_json("../../data/1000Nodes.json") is True, "The save process failed"
    #     # assert graph_algo.load_from_json("../../data/10000Nodes.json") is True, "10000 nodes went wrong"
    #     # assert graph_algo.save_to_json("../../data/10000Nodes.json") is True, "The save process failed"

    def test_get_graph(self):
        graph_algo = GraphAlgo()
        assert graph_algo.get_graph().mode_count == 0, "returned graph instead of None"
        if graph_algo.load_from_json(self.json_object) is True:
            assert isinstance(graph_algo.get_graph(), GraphInterface.GraphInterface), "returned graph instead of None"

    def test_shortest_path(self):
        graph_algo = GraphAlgo()
        graph_algo.load_from_json(self.json_object)

        dist, path = graph_algo.shortest_path(0, 7)
        # print(path)
        self.assertEqual(dist, 5.653293226161572)
        self.assertEqual([0, 10, 9, 8, 7], path)

        dist, path = graph_algo.shortest_path(0, 8888887)
        # print(path)
        self.assertEqual(dist, float(('inf')))
        self.assertEqual(path, [])

        """
        the below tests were used to determine the runTime for graphs with 1000 and 10000 nodes.
        no need to run them -> needed files are not included.
        """

        # graph_algo.load_from_json("../../data/1000Nodes.json")
        # dist, path = graph_algo.shortest_path(0, 887)
        # print(dist, path)

        # graph_algo.load_from_json("../../data/10000Nodes.json")
        # dist, path = graph_algo.shortest_path(74, 8587)
        # print(dist, path)

    def test_TSP(self):
        graph_algo = GraphAlgo()
        graph_algo.load_from_json(self.json_object)

        path, dist = graph_algo.TSP([0, 1, 2, 3, 4, 7])
        self.assertEqual(dist, 10.240617338114607)
        self.assertEqual(path, [0, 1, 2, 3, 4, 5, 6, 7])

        """
        the below tests were used to determine the runTime for graphs with 1000 and 10000 nodes.
        no need to run them -> needed files are not included.
        """
        # graph_algo.load_from_json("../../data/1000Nodes.json")
        # path, dist = graph_algo.TSP([0, 2, 5, 58, 585, 684, 245, 87, 9, 54, 244, 100, 787, 765, 20, 411, 24, 7])
        # assert dist is not None, "should've returned a float number representing the distance of the path"
        # assert path is not None, "should've returned a list og int representing the path"

        # graph_algo.load_from_json("../../data/10000Nodes.json")
        # path, dist = graph_algo.TSP([0, 2, 5, 58, 5854, 684, 245, 87, 9, 54, 244, 100, 787, 7865, 20, 411, 24, 7])
        # assert dist is not None, "should've returned a float number representing the distance of the path"
        # assert path is not None, "should've returned a list og int representing the path"

    def test_centerPoint(self):
        graph_algo = GraphAlgo()
        graph_algo.load_from_json(self.json_object)
        center, dist = graph_algo.centerPoint()
        self.assertEqual(center, 7)
        self.assertEqual(dist, 6.806805834715163)

        """
        the below tests were used to determine the runTime for graphs with 1000 and 10000 nodes.
        no need to run them -> needed files are not included.
        """
        # graph_algo.load_from_json("../../data/1000Nodes.json")
        # center, dist = graph_algo.centerPoint()
        # self.assertEqual(center, 362)
        #
        # graph_algo.load_from_json("../../data/10000Nodes.json")
        # center, dist = graph_algo.centerPoint()
        # self.assertEqual(center, 3846)

    # def test_plot_graph(self):
    #     graph_algo = GraphAlgo()
    #     graph_algo.load_from_json("../../data/A2.json")
    #     graph_algo.plot_graph()
    #     graph_algo.get_graph().remove_node(5)
    #     graph_algo.get_graph().remove_node(4)
    #     graph_algo.get_graph().remove_node(3)
    #     graph_algo.get_graph().remove_node(7)
    #     graph_algo.get_graph().remove_node(20)
    #     graph_algo.get_graph().remove_node(15)
    #     graph_algo.plot_graph()
    #     graph_algo.load_from_json("../../data/T0.json")
    #     graph_algo.plot_graph()


if __name__ == '__main__':
    unittest.main()
