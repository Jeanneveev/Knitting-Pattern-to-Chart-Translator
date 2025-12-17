import unittest
from src.domain.pattern.entities import ExpandedRow, Stitch, ExpandedRow, Pattern
from src.domain.chart.entities.chart import CellType, CellStitchType, Cell, ChartRow, Chart

STITCH = CellType.STITCH
EMPTY = CellType.EMPTY
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
        empty_cell = Cell(CellType.EMPTY)
        self.assertEqual(empty_cell.symbol, "X", None)
    
    def test_stitch_cells_must_have_given_value(self):
        try:
            valid_cell = Cell(CellType.STITCH, " ", CellStitchType.REGULAR)
        except:
            self.fail("Could not create cell")

        with self.assertRaises(ValueError) as err:
            Cell(CellType.STITCH, st_type=CellStitchType.REGULAR)
        self.assertEqual("Stitch cells must be initialized with a symbol", str(err.exception))

    def test_stitch_cells_must_have_given_cell_stitch_type(self):
        try:
            valid_cell = Cell(CellType.STITCH, "Y", CellStitchType.INCREASE)
        except:
            self.fail("Could not create cell")

        with self.assertRaises(ValueError) as err:
            Cell(CellType.STITCH, "-")
        self.assertEqual("Stitch cells must be initialized with a stitch type", str(err.exception))

    def test_cell_can_be_padded_evenly(self):
        cell = Cell(CellType.STITCH, "-", CellStitchType.REGULAR)

        expected = " - "
        actual = cell.pad_cell(2)

        self.assertEqual(expected, actual)

    def test_cell_can_be_padded_unevenly(self):
        cell = Cell(CellType.STITCH, "-", CellStitchType.REGULAR)

        expected = "   -  "
        actual = cell.pad_cell(5)

        self.assertEqual(expected, actual)

class TestChartRow(unittest.TestCase):
    def test_can_build_rs_chart_row_on_initialization(self):
        row = ExpandedRow(1, [Stitch("k"), Stitch("p")])
        chart_row = ChartRow(row)

        expected = [Cell(CellType.STITCH, "-", CellStitchType.REGULAR), Cell(CellType.STITCH, " ", CellStitchType.REGULAR)]
        actual = chart_row.cells

        self.assertEqual(expected, actual)

    def test_can_build_ws_chart_row_on_initialization(self):
        row = ExpandedRow(2, [Stitch("k"), Stitch("p"), Stitch("yo")])
        chart_row = ChartRow(row)

        expected = [
            Cell(CellType.STITCH, "-", CellStitchType.REGULAR),
            Cell(CellType.STITCH, " ", CellStitchType.REGULAR),
            Cell(CellType.STITCH, "O", CellStitchType.INCREASE)
        ]
        actual = chart_row.cells

        self.assertEqual(expected, actual)

    def test_can_get_chart_row_width(self):
        row = ExpandedRow(2, [Stitch("k"), Stitch("p"), Stitch("yo")])
        chart_row = ChartRow(row)

        expected = 3
        actual = chart_row.width

        self.assertEqual(expected, actual)

    def test_can_pad_only_left_side_of_chart_row(self):
        row = ExpandedRow(1, [Stitch("k"), Stitch("p")])
        chart_row = ChartRow(row)

        expected = [
            Cell(EMPTY), Cell(EMPTY),
            Cell(STITCH, "-", CellStitchType.REGULAR), Cell(STITCH, " ", CellStitchType.REGULAR)
        ]
        actual = chart_row.pad_row(2, 0)

        self.assertEqual(expected, actual)

    def test_can_pad_only_right_side_of_chart_row(self):
        row = ExpandedRow(1, [Stitch("k"), Stitch("p")])
        chart_row = ChartRow(row)

        expected = [
            Cell(STITCH, "-", CellStitchType.REGULAR), Cell(STITCH, " ", CellStitchType.REGULAR),
            Cell(EMPTY)
        ]
        actual = chart_row.pad_row(0, 1)

        self.assertEqual(expected, actual)

    def test_can_pad_both_sides_of_chart_row(self):
        row = ExpandedRow(1, [Stitch("k"), Stitch("p")])
        chart_row = ChartRow(row)

        expected = [
            Cell(EMPTY),
            Cell(STITCH, "-", CellStitchType.REGULAR), Cell(STITCH, " ", CellStitchType.REGULAR),
            Cell(EMPTY), Cell(EMPTY), Cell(EMPTY)
        ]
        actual = chart_row.pad_row(1, 3)

        self.assertEqual(expected, actual)

    def test_padding_chart_row_modifies_cells(self):
        row = ExpandedRow(1, [Stitch("k"), Stitch("p")])
        chart_row = ChartRow(row)
        chart_row.pad_row(1, 3)

        expected = [
            Cell(EMPTY),
            Cell(STITCH, "-", CellStitchType.REGULAR), Cell(STITCH, " ", CellStitchType.REGULAR),
            Cell(EMPTY), Cell(EMPTY), Cell(EMPTY)
        ]
        actual = chart_row.cells

        self.assertEqual(expected, actual)

    def test_can_get_if_chart_row_has_padding(self):
        row = ExpandedRow(1, [Stitch("k"), Stitch("p")])
        chart_row = ChartRow(row)
        chart_row.pad_row(1, 1)

        expected = True
        actual = chart_row.has_padding

        self.assertEqual(expected, actual)
    
    def test_can_get_left_padding_counts(self):
        row = ExpandedRow(1, [Stitch("k"), Stitch("p")])
        chart_row = ChartRow(row)
        chart_row.pad_row(1, 0)

        expected = 1
        actual = chart_row.get_padding_counts()["left"]

        self.assertEqual(expected, actual)

    def test_can_get_right_padding_counts(self):
        row = ExpandedRow(1, [Stitch("k"), Stitch("p")])
        chart_row = ChartRow(row)
        chart_row.pad_row(0, 2)

        expected = 2
        actual = chart_row.get_padding_counts()["right"]

        self.assertEqual(expected, actual)

    def test_can_get_both_padding_counts(self):
        row = ExpandedRow(1, [Stitch("k"), Stitch("p")])
        chart_row = ChartRow(row)
        chart_row.pad_row(3, 2)

        expected = {"left": 3, "right": 2}
        actual = chart_row.get_padding_counts()

        self.assertEqual(expected, actual)

class TestChart(unittest.TestCase):
    def test_can_build_chart_rows_on_initialization(self):
        pattern = Pattern([
            ExpandedRow(1, [Stitch("k"), Stitch("k")]),
            ExpandedRow(2, [Stitch("p"), Stitch("p")]),
            ExpandedRow(3, [Stitch("k"), Stitch("k")])
        ])
        chart = Chart(pattern)

        expected = [ChartRow(pattern.rows[0]), ChartRow(pattern.rows[1]), ChartRow(pattern.rows[2])]
        actual = chart.rows

        self.assertEqual(expected, actual)

    def test_can_get_chart_width(self):
        pattern = Pattern([
            ExpandedRow(1, [Stitch("k"), Stitch("k")]),
            ExpandedRow(2, [Stitch("p"), Stitch("p"), Stitch("yo")]),
        ])
        chart = Chart(pattern)

        expected = 3
        actual = chart.width

        self.assertEqual(expected, actual)

    def test_can_get_chart_height(self):
        pattern = Pattern([
            ExpandedRow(1, [Stitch("k"), Stitch("k")]),
            ExpandedRow(2, [Stitch("p"), Stitch("p"), Stitch("yo")]),
        ])
        chart = Chart(pattern)

        expected = 2
        actual = chart.height

        self.assertEqual(expected, actual)

    def test_can_get_length_of_longest_cell_value(self):
        pattern = Pattern([
            ExpandedRow(1, [Stitch("k"), Stitch("k")]),
            ExpandedRow(2, [Stitch("p"), Stitch("p")]),
            ExpandedRow(3, [Stitch("ssp")])
        ])
        chart = Chart(pattern)

        expected = 2    # ssp = \.
        actual = chart.get_max_cell_length()

        self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()