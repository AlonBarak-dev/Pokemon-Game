import unittest

from client_python.pokemon import Pokemon


class TestPokemon(unittest.TestCase):
    poke_json = {
        "value": 5.0,
        "type": -1,
        "pos": "35.197656770719604,32.10191878639921,0.0"
    }

    def test_from_dict(self):
        pokemon = Pokemon.from_dict_pok(self.poke_json, 0)
        assert pokemon.value == 5, "fail"
        assert pokemon.type == -1, "fail"
        assert pokemon.key == 0, "fail"



if __name__ == '__main__':
    unittest.main()