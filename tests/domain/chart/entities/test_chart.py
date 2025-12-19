import unittest
from src.domain.pattern.entities import ExpandedRow, Stitch, ExpandedRow, Pattern
from src.domain.chart.entities.chart import CellType, Cell, ChartRow, Chart, RowAnalysis


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
            valid_cell = Cell(CellType.STITCH, " ")
        except:
            self.fail("Could not create cell")

        with self.assertRaises(ValueError) as err:
            Cell(CellType.STITCH)
        self.assertEqual("Stitch cells must be initialized with a symbol", str(err.exception))

    def test_cell_can_be_padded_evenly(self):
        cell = Cell(CellType.STITCH, "-")

        expected = " - "
        actual = cell.pad_cell(2)

        self.assertEqual(expected, actual)

    def test_cell_can_be_padded_unevenly(self):
        cell = Cell(CellType.STITCH, "-")

        expected = "   -  "
        actual = cell.pad_cell(5)

        self.assertEqual(expected, actual)

class TestChartRow(unittest.TestCase):
    def test_can_build_rs_chart_row_on_initialization(self):
        row = ExpandedRow(1, [Stitch("k"), Stitch("p")])
        chart_row = ChartRow(row)

        expected = [Cell(CellType.STITCH, "-"), Cell(CellType.STITCH, " ")]
        actual = chart_row.cells

        self.assertEqual(expected, actual)

    def test_can_build_ws_chart_row_on_initialization(self):
        row = ExpandedRow(2, [Stitch("k"), Stitch("p"), Stitch("yo")])
        chart_row = ChartRow(row)

        expected = [
            Cell(CellType.STITCH, "-"),
            Cell(CellType.STITCH, " "),
            Cell(CellType.STITCH, "O")
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
            Cell(STITCH, "-"), Cell(STITCH, " ")
        ]
        actual = chart_row.pad_row(2, 0)

        self.assertEqual(expected, actual)

    def test_can_pad_only_right_side_of_chart_row(self):
        row = ExpandedRow(1, [Stitch("k"), Stitch("p")])
        chart_row = ChartRow(row)

        expected = [
            Cell(STITCH, "-"), Cell(STITCH, " "),
            Cell(EMPTY)
        ]
        actual = chart_row.pad_row(0, 1)

        self.assertEqual(expected, actual)

    def test_can_pad_both_sides_of_chart_row(self):
        row = ExpandedRow(1, [Stitch("k"), Stitch("p")])
        chart_row = ChartRow(row)

        expected = [
            Cell(EMPTY),
            Cell(STITCH, "-"), Cell(STITCH, " "),
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
            Cell(STITCH, "-"), Cell(STITCH, " "),
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

class TestRowAnalysis(unittest.TestCase):
    def test_can_get_ordered_stitches(self):
        row_1 = ExpandedRow(1, [Stitch("k"), Stitch("yo")])
        row_2 = ExpandedRow(2, [Stitch("k"), Stitch("yo")])
        ra_1 = RowAnalysis(row_1)
        ra_2 = RowAnalysis(row_2)

        expected_1 = [Stitch("yo"), Stitch("k")]
        expected_2 = [Stitch("k"), Stitch("yo")]
        actual_1 = ra_1.ordered_stitches
        actual_2 = ra_2.ordered_stitches

        self.assertEqual(expected_1, actual_1)
        self.assertEqual(expected_2, actual_2)

    def test_can_get_left_growth(self):
        row = ExpandedRow(1, [Stitch("k"), Stitch("kfb")])
        row_analysis = RowAnalysis(row)

        expected_l_growth = 1
        actual_l_growth = row_analysis.left_growth

        self.assertEqual(expected_l_growth, actual_l_growth)

    def test_can_get_right_growth(self):
        row = ExpandedRow(1, [Stitch("k"), Stitch("kfb")])
        row_analysis = RowAnalysis(row)

        expected_r_growth = 0
        actual_r_growth = row_analysis.right_growth

        self.assertEqual(expected_r_growth, actual_r_growth)

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

    # def test_can_build_row_analyses_on_initialization(self):
    #     r_1 = ExpandedRow(1, [Stitch("k"), Stitch("k")])
    #     r_2 = ExpandedRow(2, [Stitch("p"), Stitch("p")])
    #     r_3 = ExpandedRow(3, [Stitch("k"), Stitch("k")])
    #     chart = Chart(Pattern([r_1, r_2, r_3]))

    #     expected = [RowAnalysis(r_1, 0), RowAnalysis(r_2, 0), RowAnalysis(r_3, 0)]
    #     actual = chart.row_analyses

    #     self.assertEqual(expected, actual)

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

    def test_can_maximum_row_left_width(self):
        chart = Chart(Pattern([
            ExpandedRow(1, [Stitch("k"), Stitch("k"), Stitch("yo")]),
            ExpandedRow(2, [Stitch("kfb"), Stitch("yo"), Stitch("p"), Stitch("p")]),
        ]))

        expected = 2
        actual = chart.max_left

        self.assertEqual(expected, actual)

    def test_can_maximum_row_right_width(self):
        chart = Chart(Pattern([
            ExpandedRow(1, [Stitch("k"), Stitch("k"), Stitch("yo")]),
            ExpandedRow(2, [Stitch("kfb"), Stitch("yo"), Stitch("p"), Stitch("p"), Stitch("yo")]),
        ]))

        expected = 2
        actual = chart.max_right

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

    def test_can_pad_chart(self):
        self.maxDiff = None
        
        row_1 = ExpandedRow(1, [Stitch("k"), Stitch("kfb")])
        row_2 = ExpandedRow(2, [Stitch("p"), Stitch("p"), Stitch("p")])
        pattern = Pattern([row_1, row_2])
        chart = Chart(pattern)
        chart.pad_chart()

        """ Chart should look like:
            "---+---+---+---+---\n"
            " 2 |   |   |   |   \n"
            "---+---+---+---+---\n"
            "   | X | Y |   | 1 \n"
            "---+---+---+---+---\n"
        """

        expected_row_1 = [Cell(EMPTY), Cell(STITCH, "Y"), Cell(STITCH, " ")]
        expected_row_2 = [Cell(STITCH, " "), Cell(STITCH, " "), Cell(STITCH, " ")]
        actual_row_1 = chart.rows[0].cells
        actual_row_2 = chart.rows[1].cells

        self.assertEqual(expected_row_1, actual_row_1)
        self.assertEqual(expected_row_2, actual_row_2)

    def test_can_pad_chart_2(self):
        row_1 = ExpandedRow(1, [Stitch("kfb"), Stitch("k")])
        row_2 = ExpandedRow(2, [Stitch("p"), Stitch("p"), Stitch("p")])
        pattern = Pattern([row_1, row_2])
        chart = Chart(pattern)
        chart.pad_chart()

        """ Chart should look like:
            "---+---+---+---+---\n"
            " 2 |   |   |   |   \n"
            "---+---+---+---+---\n"
            "   |   | Y | X | 1 \n"
            "---+---+---+---+---\n"
        """
        
        expected_row_1 = [Cell(STITCH, " "), Cell(STITCH, "Y"), Cell(EMPTY)]
        expected_row_2 = [Cell(STITCH, " "), Cell(STITCH, " "), Cell(STITCH, " ")]
        actual_row_1 = chart.rows[0].cells
        actual_row_2 = chart.rows[1].cells

        self.assertEqual(expected_row_1, actual_row_1)
        self.assertEqual(expected_row_2, actual_row_2)

if __name__ == "__main__":
    unittest.main()