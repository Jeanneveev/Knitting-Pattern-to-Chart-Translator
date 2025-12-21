import unittest
from src.domain.pattern.entities import ExpandedRow, Stitch, ExpandedRow, Pattern
from src.domain.chart.entities.chart import CellType, Cell, ChartRow, Chart

class TestChartCell(unittest.TestCase):
    def test_cell_type_has_limited_values(self):
        cell_types = ["empty", "stitch"]
        for t in cell_types:
            self.assertNotEqual(None, CellType(t))

        invalid_type = "-"
        with self.assertRaises(ValueError) as err:
            CellType(invalid_type)
        self.assertEqual(f"'{invalid_type}' is not a valid CellType", str(err.exception))

    def test_empty_cells_have_automatic_value(self):
        empty_cell = Cell("ANY", 0, 1, CellType.EMPTY)
        self.assertEqual(empty_cell.symbol, "X")    

class TestChart(unittest.TestCase):
    def test_chart_initializes_with_rows(self):
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

        expected_row_1 = ChartRow(1, [
            Cell(" ", 0, 1), Cell(" ", 1, 2),
            Cell("-", 2, 3), Cell("-", 3, 4),
            Cell(" ", 4, 5)
        ])
        expected_row_2 = ChartRow(2, [
            Cell("-", 0, 1),
            Cell(" ", 1, 2), Cell(" ", 2, 3),
            Cell("-", 3, 4), Cell("-", 4, 5)
        ])
        expected_row_3 = ChartRow(3, [
            Cell(" ", 0, 1), Cell(" ", 1, 2),
            Cell("-", 2, 3), Cell("-", 3, 4),
            Cell(" ", 4, 5)
        ])

        actual = chart.rows
        actual_row_1 = actual[0]
        actual_row_2 = actual[1]
        actual_row_3 = actual[2]

        self.assertEqual(expected_row_1, actual_row_1)
        self.assertEqual(expected_row_2, actual_row_2)
        self.assertEqual(expected_row_3, actual_row_3)

    def test_chart_initializes_with_right_aligned_rows(self):
        row_1 = ExpandedRow(3, [Stitch("kfb"), Stitch("k")])
        row_2 = ExpandedRow(4, [Stitch("p"), Stitch("p"), Stitch("p")])
        pattern = Pattern([row_1, row_2])
        chart = Chart(pattern)

        """ Chart should look like:
            "---+---+---+---+---\n"
            " 4 |   |   |   |   \n"
            "---+---+---+---+---\n"
            "   | X |   | Y | 3 \n"
            "---+---+---+---+---\n"
        """

        expected_row_1 = ChartRow(3, [Cell("Y", 0, 1), Cell(" ", 1, 2)])
        expected_row_2 = ChartRow(4, [Cell(" ", 0, 1), Cell(" ", 1, 2), Cell(" ", 2, 3)])

        actual = chart.rows
        actual_row_1 = actual[0]
        actual_row_2 = actual[1]

        self.assertEqual(expected_row_1, actual_row_1)
        self.assertEqual(expected_row_2, actual_row_2)

    def test_chart_initializes_with_key_dictionary(self):
        row_1 = ExpandedRow(3, [Stitch("kfb"), Stitch("k")])
        row_2 = ExpandedRow(4, [Stitch("p"), Stitch("p"), Stitch("p")])
        chart = Chart(Pattern([row_1, row_2]))

        expected = {
            " ": {"rs": "knit", "ws": "purl"},
            "Y": {"rs": "knit in front and back", "ws": "knit in front and back"}
        }
        actual = chart.key

        self.assertEqual(expected, actual)

    def test_can_get_chart_row_by_number(self):
        row_1 = ExpandedRow(3, [Stitch("kfb"), Stitch("k")])
        row_2 = ExpandedRow(4, [Stitch("p"), Stitch("p"), Stitch("p")])
        pattern = Pattern([row_1, row_2])
        chart = Chart(pattern)

        expected = ChartRow(3, [Cell("Y", 0, 1), Cell(" ", 1, 2)])
        actual = chart.get_row(3)

        self.assertEqual(expected, actual)

    def test_cant_get_nonexistent_chart_row_number(self):
        row_1 = ExpandedRow(1, [Stitch("kfb"), Stitch("k")])
        row_2 = ExpandedRow(2, [Stitch("p"), Stitch("p"), Stitch("p")])
        pattern = Pattern([row_1, row_2])
        chart = Chart(pattern)

        with self.assertRaises(ValueError) as err:
            chart.get_row(3)

        self.assertEqual("No chart row of number: 3 found", str(err.exception))

    def test_can_shift_specific_row_left(self):
        pattern = Pattern([
            ExpandedRow(5, [
                Stitch("kfb"), Stitch("k"), Stitch("k"), Stitch("kfb")
            ]),
            ExpandedRow(6, [
                Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p")
            ]),
            ExpandedRow(7, [
                Stitch("kfb"), Stitch("k"), Stitch("k"), Stitch("k"), Stitch("k"), Stitch("kfb")
            ]),
            ExpandedRow(8, [
                Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p")
            ])
        ])
        chart = Chart(pattern)

        """ Chart should look like:
            "---+---+---+---+---+---+---+---+---+---\n"
            " 8 |   |   |   |   |   |   |   |   |   \n"
            "---+---+---+---+---+---+---+---+---+---\n"
            "   | X | X | Y |   |   |   |   | Y | 7 \n"
            "---+---+---+---+---+---+---+---+---+---\n"
            " 6 | X | X |   |   |   |   |   |   |   \n"
            "---+---+---+---+---+---+---+---+---+---\n"
            "   | X | X | X | X | Y |   |   | Y | 5 \n"
            "---+---+---+---+---+---+---+---+---+---\n"
        """

        chart.shift_row_left(6, 2)

        expected = ChartRow(6, [
            Cell(" ", 2, 3), Cell(" ", 3, 4),
            Cell(" ", 4, 5), Cell(" ", 5, 6),
            Cell(" ", 6, 7), Cell(" ", 7, 8),
        ])
        actual = chart.get_row(6)

        self.assertEqual(expected, actual)

    def test_cannot_shift_left_past_chart_width(self):
        pattern = Pattern([
            ExpandedRow(5, [
                Stitch("kfb"), Stitch("k"), Stitch("k"), Stitch("kfb")
            ]),
            ExpandedRow(6, [
                Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p")
            ]),
            ExpandedRow(7, [
                Stitch("kfb"), Stitch("k"), Stitch("k"), Stitch("k"), Stitch("k"), Stitch("kfb")
            ]),
            ExpandedRow(8, [
                Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p")
            ])
        ])
        chart = Chart(pattern)

        with self.assertRaises(IndexError) as err:
            chart.shift_row_left(8, 1)

        self.assertEqual("Shift goes beyond chart bounds", str(err.exception))

    def test_can_shift_specific_row_left(self):
        pattern = Pattern([
            ExpandedRow(1, [
                Stitch("ssk"),
                Stitch("k"), Stitch("k"), Stitch("k"), Stitch("k"), Stitch("k"), Stitch("k"),
                Stitch("k2tog")
            ]),
            ExpandedRow(2, [
                Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p")
            ]),
            ExpandedRow(3, [
                Stitch("ssk"),
                Stitch("k"), Stitch("k"), Stitch("k"), Stitch("k"),
                Stitch("k2tog")
            ]),
            ExpandedRow(4, [
                Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p")
            ]),
            ExpandedRow(5, [
                Stitch("ssk"),
                Stitch("k"), Stitch("k"),
                Stitch("k2tog")
            ])
        ])
        chart = Chart(pattern)

        """ Chart should look like:
            "---+---+---+---+---+---+---+---+---+---\n"
            "   | X | X | X | X | / |   |   | \\ | 5 \n"
            "---+---+---+---+---+---+---+---+---+---\n"
            " 4 | X | X |   |   |   |   |   |   |   \n"
            "---+---+---+---+---+---+---+---+---+---\n"
            "   | X | X | / |   |   |   |   | \\ | 3 \n"
            "---+---+---+---+---+---+---+---+---+---\n"
            " 2 |   |   |   |   |   |   |   |   |   \n"
            "---+---+---+---+---+---+---+---+---+---\n"
            "   | / |   |   |   |   |   |   | \\ | 1 \n"
            "---+---+---+---+---+---+---+---+---+---\n"
        """

        chart.shift_row_left(5, 3)
        chart.shift_row_right(5, 1)
        # +2
        expected = ChartRow(5, [
            Cell("\\", 2, 3), Cell(" ", 3, 4),
            Cell(" ", 4, 5), Cell("/", 5, 6),
        ])
        actual = chart.get_row(5)

        self.assertEqual(expected, actual)

    def test_cannot_shift_right_past_chart_width(self):
        pattern = Pattern([
            ExpandedRow(1, [
                Stitch("ssk"),
                Stitch("k"), Stitch("k"), Stitch("k"), Stitch("k"), Stitch("k"), Stitch("k"),
                Stitch("k2tog")
            ]),
            ExpandedRow(2, [
                Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p")
            ]),
            ExpandedRow(3, [
                Stitch("ssk"),
                Stitch("k"), Stitch("k"), Stitch("k"), Stitch("k"),
                Stitch("k2tog")
            ]),
            ExpandedRow(4, [
                Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p")
            ]),
            ExpandedRow(5, [
                Stitch("ssk"),
                Stitch("k"), Stitch("k"),
                Stitch("k2tog")
            ])
        ])
        chart = Chart(pattern)

        with self.assertRaises(IndexError) as err:
            chart.shift_row_right(2, 1)

        self.assertEqual("Shift goes beyond chart bounds", str(err.exception))

    def test_can_pad_row_to_given_width_one_side(self):
        pattern = Pattern([
            ExpandedRow(1, [Stitch("p"), Stitch("p"), Stitch("p")]),
            ExpandedRow(2, [Stitch("s2kp2")]),
            ExpandedRow(3, [Stitch("p")]),
        ])
        chart = Chart(pattern)

        """ Chart should look like:
            "---+---+---+---+---\n"
            " 2 | X | X | ^ |   \n"
            "---+---+---+---+---\n"
        """
        expected = ChartRow(2, [
            Cell("^", 0, 1),
            Cell("X", 1, 2, CellType.EMPTY),
            Cell("X", 2, 3, CellType.EMPTY)
        ])
        actual = chart.get_padded_row(2, chart.width)

        self.assertEqual(expected, actual)

    def test_can_pad_row_to_given_width_both_sides(self):
        pattern = Pattern([
            ExpandedRow(1, [Stitch("p"), Stitch("p"), Stitch("p")]),
            ExpandedRow(2, [Stitch("s2kp2")]),
            ExpandedRow(3, [Stitch("p")]),
        ])
        chart = Chart(pattern)
        chart.shift_row_left(3, 1)

        """ Chart should look like:
            "---+---+---+---+---\n"
            "   | X | - | X | 3 \n"
            "---+---+---+---+---\n"
        """
        expected = ChartRow(3, [
            Cell("X", 0, 1, CellType.EMPTY),
            Cell("-", 1, 2),
            Cell("X", 2, 3, CellType.EMPTY)
        ])
        actual = chart.get_padded_row(3, chart.width)

        self.assertEqual(expected, actual)

    def test_can_pad_row_of_equal_given_width_does_nothing(self):
        pattern = Pattern([
            ExpandedRow(1, [Stitch("p"), Stitch("p"), Stitch("p")]),
            ExpandedRow(2, [Stitch("s2kp2")]),
            ExpandedRow(3, [Stitch("p")]),
        ])
        chart = Chart(pattern)

        """ Chart should look like:
            "---+---+---+---+---\n"
            "   | - | - | - | 1 \n"
            "---+---+---+---+---\n"
        """

        expected = ChartRow(1, [
            Cell("-", 0, 1),
            Cell("-", 1, 2),
            Cell("-", 2, 3)
        ])
        actual = chart.get_padded_row(1, chart.width)

        self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()