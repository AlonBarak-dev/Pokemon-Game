import unittest

from client_python.Agent import Agent


class TestPokemon(unittest.TestCase):
    agent_json = {
        "id": 0,
        "value": 0.0,
        "src": 0,
        "dest": 1,
        "speed": 1.0,
        "pos": "35.18753053591606,32.10378225882353,0.0"
    }

    def test_from_dict(self):
        agent = Agent.from_dict(self.agent_json)
        assert agent.id == 0, "fail"
        assert agent.value == 0.0, "fail"
        assert agent.src == 0, "fail"
        assert agent.dest == 1, "fail"
        assert agent.speed == 1.0, "fail"

if __name__ == '__main__':
    unittest.main()
