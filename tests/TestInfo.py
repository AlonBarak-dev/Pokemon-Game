import unittest

from client_python.Info import Info


class TestPokemon(unittest.TestCase):
    info_json = {
            "GameServer":{
                "pokemons":1,
                "is_logged_in":"false",
                "moves":1,
                "grade":0,
                "game_level":0,
                "max_user_level":-1,
                "id":0,
                "graph":"data/A0",
                "agents":1
            }
        }

    def test_from_dict(self):
        info = Info.from_dict(self.info_json)
        assert info.pokemons == 1, "fail"
        assert info.id == 0, "fail"
        assert info.graph is "data/A0", "fail"
        assert info.agents == 1, "fail"
        assert info.game_level == 0, "fail"


if __name__ == '__main__':
    unittest.main()
