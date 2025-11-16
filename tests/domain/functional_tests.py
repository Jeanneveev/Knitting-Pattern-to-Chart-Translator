"""Tests that span across the entire core"""

import unittest
from src.domain.parser.parser import Parser
from src.domain.model.model import Chart

class TestBackend(unittest.TestCase):
    def test_can_translate_input_to_chart(self):
        input = (
            "cast on 6 sts\n"
            "row 1: k2, p2, k2\n"
            "row 2: p2, k2, p2\n"
            "row 3: *k, p* \n"
            "row 4: *p, k*; repeat from * to * 3 times"
        )
        parser = Parser(input)
        model_obj = parser.start()
        chart = Chart(model_obj)

        expected = (
            "---+---+---+---+---+---+---+---\n"
            " 4 |   | - |   | - |   | - |   \n"
            "---+---+---+---+---+---+---+---\n"
            "   | - |   | - |   | - |   | 3 \n"
            "---+---+---+---+---+---+---+---\n"
            " 2 |   |   | - | - |   |   |   \n"
            "---+---+---+---+---+---+---+---\n"
            "   |   |   | - | - |   |   | 1 \n"
            "---+---+---+---+---+---+---+---"
        )
        actual = chart.render_grid()

        self.assertEqual(expected, actual, f"expected was:\n{expected}\nactual was:\n{actual}")

if __name__ == "__main__":
    unittest.main()