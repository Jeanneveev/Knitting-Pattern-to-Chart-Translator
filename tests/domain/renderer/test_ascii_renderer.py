import unittest
from src.domain.pattern.entities import Pattern, ExpandedRow, Stitch
from src.domain.chart.entities.chart import Chart, ChartRow, Cell, CellType
from src.domain.renderer.ascii_renderer import ASCIIRender


class TestASCIIChart(unittest.TestCase):
    def test_can_create_padded_rows(self):
        pattern = Pattern([
            ExpandedRow(1, [
                Stitch("kfb"), Stitch("k"), Stitch("k"), Stitch("kfb")
            ]),
            ExpandedRow(2, [
                Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p")
            ])
        ])
        chart = Chart(pattern)
        renderer = ASCIIRender(chart)

        """ Chart should look like:
            "---+---+---+---+---+---+---+---\n"
            " 2 |   |   |   |   |   |   |   \n"
            "---+---+---+---+---+---+---+---\n"
            "   | X | X | Y |   |   | Y | 1 \n"
            "---+---+---+---+---+---+---+---\n"
        """

        renderer._add_padding()
        
        expected_row_1 = ChartRow(1, [
            Cell("Y", 0, 1),
            Cell(" ", 1, 2), Cell(" ", 2, 3),
            Cell("Y", 3, 4),
            Cell("X", 4, 5, CellType.EMPTY), Cell("X", 5, 6, CellType.EMPTY)
        ])
        expected_row_2 = ChartRow(2, [
            Cell(" ", 0, 1), Cell(" ", 1, 2),
            Cell(" ", 2, 3), Cell(" ", 3, 4),
            Cell(" ", 4, 5), Cell(" ", 5, 6),
        ])

        actual = renderer.padded_rows
        actual_row_1 = actual[0]
        actual_row_2 = actual[1]

        self.assertEqual(expected_row_1, actual_row_1)
        self.assertEqual(expected_row_2, actual_row_2)

    def test_padded_rows_set_on_initialization(self):
        pattern = Pattern([
            ExpandedRow(1, [Stitch("k"), Stitch("yo")]),
            ExpandedRow(2, [Stitch("p"), Stitch("p")]),
            ExpandedRow(3, [Stitch("k2tog")])
        ])
        renderer = ASCIIRender(Chart(pattern))

        """ Chart should look like:
            "---+---+----+---\n"
            "   | X | / | 3 \n"
            "---+---+----+---\n"
            " 2 |   |    |   \n"
            "---+---+----+---\n"
            "   | O |    | 1 \n"
            "---+---+----+---\n"
        """

        expected_row_1 = ChartRow(1, [Cell(" ", 0, 1), Cell("O", 1, 2)])
        expected_row_2 = ChartRow(2, [Cell(" ", 0, 1), Cell(" ", 1, 2)])
        expected_row_3 = ChartRow(3, [Cell("/", 0, 1), Cell("X", 1, 2, CellType.EMPTY)])
        actual = renderer.padded_rows
        actual_row_1 = actual[0]
        actual_row_2 = actual[1]
        actual_row_3 = actual[2]

        self.assertEqual(expected_row_1, actual_row_1)
        self.assertEqual(expected_row_2, actual_row_2)
        self.assertEqual(expected_row_3, actual_row_3)

    def test_can_get_longest_row_symbol_length(self):
        pattern = Pattern([
            ExpandedRow(1, [Stitch("k"), Stitch("k"), Stitch("k"), Stitch("k")]),
            ExpandedRow(2, [Stitch("k"), Stitch("ssk"), Stitch("k")])
        ])
        renderer = ASCIIRender(Chart(pattern))

        expected = 2    # ssk ws = \.
        actual = renderer._get_max_row_sym_len(2)

        self.assertEqual(expected, actual)

    def test_can_get_longest_symbol_length(self):
        pattern = Pattern([
            ExpandedRow(1, [Stitch("k"), Stitch("yo")]),
            ExpandedRow(2, [Stitch("k2tog")])
        ])
        renderer = ASCIIRender(Chart(pattern))

        expected = 2    # k2tog ws = /.
        actual = renderer._get_max_chart_sym_len()

        self.assertEqual(expected, actual)

    def test_can_get_longest_symbol_length_despite_double_escape(self):
        pattern = Pattern([ExpandedRow(1, [Stitch("k"), Stitch("ssk")])])
        renderer = ASCIIRender(Chart(pattern))

        expected = 1 
        actual = renderer._get_max_chart_sym_len()

        self.assertEqual(expected, actual)

    def test_can_build_border_to_size(self):
        pattern = Pattern([
            ExpandedRow(1, [Stitch("k"), Stitch("yo"), Stitch("k")]),
            ExpandedRow(2, [Stitch("k"), Stitch("k"), Stitch("k")])
        ])
        renderer = ASCIIRender(Chart(pattern))

        expected = "---+---+---+---+---\n"
        actual = renderer._build_border()

        self.assertEqual(expected, actual)

    def test_can_evenly_pad_symbol(self):
        pattern = Pattern([ExpandedRow(1, [Stitch("p"), Stitch("p")])])
        renderer = ASCIIRender(Chart(pattern))

        expected = " - "
        actual = renderer._pad_item("-")

        self.assertEqual(expected, actual)

    def test_can_unevenly_pad_symbol(self):
        pattern = Pattern([ExpandedRow(1, [Stitch("p2tog"), Stitch("p")])])
        renderer = ASCIIRender(Chart(pattern))

        expected = "  - "
        actual = renderer._pad_item("-")

        self.assertEqual(expected, actual)

    def test_can_build_row_symbols(self):
        pattern = Pattern([
            ExpandedRow(2, [
                Stitch("k"), Stitch("k"), Stitch("p")
            ]),
            ExpandedRow(3, [
                Stitch("k"), Stitch("k"), Stitch("k")
            ]),
        ])
        renderer = ASCIIRender(Chart(pattern))

        """ Chart should look like:
            "---+---+---+---+---\n"
            "   |   |   |   | 3 \n"
            "---+---+---+---+---\n"
            " 2 | - | - |   |   \n"
            "---+---+---+---+---\n"
        """

        expected = " 2 | - | - |   |   \n"
        actual = renderer._build_row(2)

        self.assertEqual(expected, actual)

    def test_can_build_ascii_grid(self):
        self.maxDiff = None

        pattern = Pattern([
            ExpandedRow(1, [Stitch("k"), Stitch("p"), Stitch("kfb")]),
            ExpandedRow(2, [Stitch("p"), Stitch("p"), Stitch("k"), Stitch("k")]),
            ExpandedRow(3, [Stitch("ssk"), Stitch("k2tog")])
        ])
        renderer = ASCIIRender(Chart(pattern))
        
        expected = (
            "---+---+---+---+---+---\n"
            "   | X | X | / | \\ | 3 \n"
            "---+---+---+---+---+---\n"
            " 2 |   |   | - | - |   \n"
            "---+---+---+---+---+---\n"
            "   | X | Y | - |   | 1 \n"
            "---+---+---+---+---+---\n"
        )
        actual = renderer.render_ascii_chart()

        self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()