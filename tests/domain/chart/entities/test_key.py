import unittest
from src.domain.chart.entities.key import Key

class TestKey(unittest.TestCase):
    def test_can_get_canonical_key(self):
        key = Key()

        expected = {
            " ":   {"rs": "knit",                                         "ws": "purl"},
            "-":   {"rs": "purl",                                         "ws": "knit"},
            "O":   {"rs": "yarn over",                                    "ws": "yarn over"},
            "Y":   {"rs": "knit in front and back",                       "ws": "knit in front and back"},
            "/":   {"rs": "knit 2 together",                              "ws": "purl 2 together"},
            "/.":  {"rs": "purl 2 together",                              "ws": "knit 2 together"},
            "\\":  {"rs": "slip slip knit",                               "ws": "slip slip purl"},
            "\\.": {"rs": "slip slip purl",                               "ws": "slip slip knit"},
            "^":   {"rs": "slip 2, knit 1, pass 2 slipped stitches over", "ws": "slip 2, knit 1, pass 2 slipped stitches over"},
        }
        actual = key.canonical_key

        self.assertEqual(expected, actual)

    def test_can_get_passed_symbols_only_key(self):
        symbols = [" ", "-", "Y"]
        key = Key(symbols)

        expected = {
            " ":   {"rs": "knit",                   "ws": "purl"},
            "-":   {"rs": "purl",                   "ws": "knit"},
            "Y":   {"rs": "knit in front and back", "ws": "knit in front and back"},
        }
        actual = key.KEY_BY_SYMBOLS

        self.assertEqual(expected, actual)

    def test_cannot_get_key_from_unknown_symbol(self):
        symbols = [" ", "A", "-"]
        key = Key(symbols)

        with self.assertRaises(IndexError) as err:
            key.KEY_BY_SYMBOLS
        
        self.assertEqual("Symbol not found: \"A\"", str(err.exception))

if __name__ == "__main__":
    unittest.main()