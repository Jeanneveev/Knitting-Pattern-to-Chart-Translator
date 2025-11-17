import unittest
from src.domain.model.model import Part, Row, Repeat, Stitch
from src.adapters.chart_adapter import ChartAdapter

class TestChartAdapter(unittest.TestCase):
    def test_can_generate_chart_from_model(self):
        model = Part(6, [
            Row(1, [Stitch("k"), Stitch("k"), Stitch("p"), Stitch("p"), Stitch("k"), Stitch("k")])
        ])

        expected = (
            "---+---+---+---+---+---+---+---\n"
            "   |   |   | - | - |   |   | 1 \n"
            "---+---+---+---+---+---+---+---"
        )
        actual = ChartAdapter().render_chart(model)

        self.assertEqual(expected, actual)

    def test_raises_error_on_invalid_model(self):
        invalid_model = "invalid"

        with self.assertRaises(AttributeError) as err:
            ChartAdapter().render_chart(invalid_model)
        self.assertEqual("'str' object has no attribute 'pattern'", str(err.exception))

if __name__ == "__main__":
    unittest.main()