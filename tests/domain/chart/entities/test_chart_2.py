import unittest
from src.domain.pattern.entities import ExpandedRow, Stitch, ExpandedRow, Pattern
from src.domain.chart.entities.chart_2 import Cell, ChartRow, Chart

class TestChart(unittest.TestCase):
    def test_can_hypothesize_regular_next_row(self):
        row_1 = ExpandedRow(1, [Stitch("k"), Stitch("k"), Stitch("p"), Stitch("p"), Stitch("k")])
        row_2 = ExpandedRow(2, [Stitch("k"), Stitch("k"), Stitch("p"), Stitch("p"), Stitch("k")])
        row_3 = ExpandedRow(3, [Stitch("k"), Stitch("k"), Stitch("p"), Stitch("p"), Stitch("k")])
        chart = Chart(Pattern([row_1, row_2, row_3]))

        """ Chart should look like:
            "---+---+---+---+---+---+---\n"
            "   |   | - | - |   |   | 3 \n"
            "---+---+---+---+---+---+---\n"
            " 2 | - | - |   |   | - |   \n"
            "---+---+---+---+---+---+---\n"
            "   |   | - | - |   |   | 1 \n"
            "---+---+---+---+---+---+---\n"
        """

        expected_row_1 = (1, [4, 3, 2, 1])
        expected_row_2 = (2, [4, 3, 2, 1])
        expected_row_3 = (3, [4, 3, 2, 1])

        actual = chart.hypothesize_chart_rows()
        actual_row_1 = actual[0]
        actual_row_2 = actual[1]
        actual_row_3 = actual[2]

        self.assertEqual(expected_row_1, actual_row_1)
        self.assertEqual(expected_row_2, actual_row_2)
        self.assertEqual(expected_row_3, actual_row_3)


if __name__ == "__main__":
    unittest.main()