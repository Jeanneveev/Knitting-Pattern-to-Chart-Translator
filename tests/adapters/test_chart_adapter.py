import unittest
from src.domain import ASCIIRender, Chart, ExpandedRow, Pattern, Stitch
from src.adapters.chart_adapter import ChartAdapter

class TestChartAdapter(unittest.TestCase):
    def test_can_generate_chart_from_pattern(self):
        pattern = Pattern([ExpandedRow(1, [
            Stitch("k"), Stitch("k"), Stitch("p"), Stitch("p"), Stitch("k"), Stitch("k")
        ])])

        expected = (
            "---+---+---+---+---+---+---+---\n"
            "   |   |   | - | - |   |   | 1 \n"
            "---+---+---+---+---+---+---+---\n"
        )
        actual = ChartAdapter().render_chart(pattern)

        self.assertEqual(expected, actual)

    def test_raises_error_on_invalid_pattern(self):
        invalid_pattern = "invalid"

        with self.assertRaises(AttributeError) as err:
            ChartAdapter().render_chart(invalid_pattern)
        self.assertIn("Error occured when building chart:", str(err.exception))

    def test_can_generate_key_from_pattern(self):
        pattern = Pattern([
            ExpandedRow(1, [
                Stitch("k"), Stitch("k"), Stitch("p"), Stitch("k"), Stitch("k")
            ]),
            ExpandedRow(2, [
                Stitch("p"), Stitch("p"), Stitch("k"), Stitch("p"), Stitch("p")
            ])
        ])

        expected = (
            "+--------+-------------+\n"
            "| SYMBOL |   MEANING   |\n"
            "+--------+-------------+\n"
            "|        |  RS  |  WS  |\n"
            "+--------+------+------+\n"
            "|        | knit | purl |\n"
            "+--------+------+------+\n"
            "|    -   | purl | knit |\n"
            "+--------+------+------+\n"
        )
        actual = ChartAdapter().render_key(pattern)

        self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()