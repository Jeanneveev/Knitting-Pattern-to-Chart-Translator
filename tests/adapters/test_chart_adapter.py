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

    # def test_can_generate_key_from_model(self):
    #     model = Part(9, [
    #         Row(1, [Repeat([Stitch("k"), Stitch("p"), Stitch("k")], num_times=3)])
    #     ])

    #     expected = (
    #         "+------+--------+-----------+-----------+\n"
    #         "| Name | Abbrev | RS Symbol | WS Symbol |\n"
    #         "+------+--------+-----------+-----------+\n"
    #         "| Knit |    k   |           |     -     |\n"
    #         "+------+--------+-----------+-----------+\n"
    #         "| Purl |    p   |     -     |           |\n"
    #         "+------+--------+-----------+-----------+\n"
    #     )
    #     actual = ChartAdapter().render_key(model)

    #     self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()