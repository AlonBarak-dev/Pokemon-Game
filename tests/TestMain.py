import json
import os
import time
import unittest
import multiprocessing

from client_python.client import Client
from graph.DiGraph import DiGraph
from graph.GraphAlgo import GraphAlgo


def open_server():
    os.system('java -jar Ex4_Server_v0.0.jar 0')


class TestMain(unittest.TestCase):

    def test_load_from_json(self):
        process = multiprocessing.Process(target=open_server)
        start = time.time()
        process.start()
        while time.time() - start < 1:
            continue
        try:
            PORT = 6666
            HOST = '127.0.0.1'

            client = Client()
            client.start_connection(HOST, PORT)
            graph_algo = GraphAlgo(DiGraph())
            graph_algo.load_from_json(json.loads(client.get_graph()))
            self.assertNotEqual(graph_algo.graph.__repr__(), "Graph: |V|=0 , |E|=0")
            print(graph_algo.graph)
            client.stop_connection()
            os.system('exit')
        except ResourceWarning as e:
            print("Test is finished")
