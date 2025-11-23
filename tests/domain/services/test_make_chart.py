import unittest
from src.domain.services.make_chart import Chart
from src.domain.services.make_pattern import ExpandedRow, Pattern
from src.domain.model.model import Stitch

class TestChart(unittest.TestCase):
    def test_can_get_symbols_of_right_side_row(self):
        row = ExpandedRow(1, [Stitch("k"), Stitch("p"), Stitch("k"), Stitch("p")])
        pattern = Pattern([row])
        chart = Chart(pattern)

        expected = {1: ["-", " ", "-", " "]}
        actual = chart.get_row_symbols(1)

        self.assertEqual(expected, actual)
    
    def test_can_get_symbols_of_wrong_side_row(self):
        row_1 = ExpandedRow(1, [Stitch("k"), Stitch("yo"), Stitch("k")])
        # print(f"End stitch count is: {row_1.end_st_count}")
        row_2 = ExpandedRow(2, [Stitch("k"), Stitch("k2tog")])
        pattern = Pattern([row_1, row_2])
        chart = Chart(pattern)

        expected = {2: ["-", "/"]}
        actual = chart.get_row_symbols(2)

        self.assertEqual(expected, actual)

    def test_can_generate_border_of_maximum_row_length(self):
        pattern = Pattern([
            ExpandedRow(1, [Stitch("k"), Stitch("yo"), Stitch("k")]),
            ExpandedRow(2, [Stitch("k"), Stitch("k"), Stitch("k")])
        ])
        chart = Chart(pattern)

        expected = "---+---+---+---+---\n"
        actual = chart._build_border()

        self.assertEqual(expected, actual)

    def test_can_build_right_side_row(self):
        pattern = Pattern([
            ExpandedRow(1, [Stitch("k"), Stitch("yo"), Stitch("k")]),
            ExpandedRow(2, [Stitch("k"), Stitch("k"), Stitch("k")])
        ])
        chart = Chart(pattern)

        expected = "   |   | O |   | 1 \n"
        actual = chart._build_row(1)

        self.assertEqual(expected, actual)

    def test_can_build_wrong_side_row(self):
        pattern = Pattern([
            ExpandedRow(1, [Stitch("k"), Stitch("yo"), Stitch("k")]),
            ExpandedRow(2, [Stitch("k"), Stitch("k"), Stitch("k")])
        ])
        chart = Chart(pattern)

        expected = " 2 | - | - | - |   \n"
        actual = chart._build_row(2)

        self.assertEqual(expected, actual)

    def test_can_generate_1_row_chart_from_pattern(self):
        pattern = Pattern([
            ExpandedRow(1, [Stitch("k"), Stitch("k"), Stitch("p"), Stitch("p")])
        ])
        chart = Chart(pattern)

        expected = (
            "---+---+---+---+---+---\n"
            "   | - | - |   |   | 1 \n"
            "---+---+---+---+---+---\n"
        )
        actual = chart.render_grid()

        self.assertEqual(expected, actual)

    def test_can_generate_1_row_chart_w_increases_and_decreases(self):
        # row 1: (k, p) x 2, k2, ssk, k2tog, (k, yo) x 2, k, p, k
        row = ExpandedRow(1, [
            Stitch("k"), Stitch("p"), Stitch("k"), Stitch("p"),
            Stitch("k"), Stitch("k"),
            Stitch("ssk"), Stitch("k2tog"),
            Stitch("k"), Stitch("yo"), Stitch("k"), Stitch("yo"),
            Stitch("k"), Stitch("p"), Stitch("k")
        ])
        chart = Chart(Pattern([row]))

        expected = (    # NOTE: ssk box lines up when printed
            "---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---\n"
            "   |   | - |   | O |   | O |   | / | \\ |   |   | - |   | - |   | 1 \n"
            "---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---\n"
        )
        actual = chart.render_grid()

        # print(f"Expected is:\n{expected}")

        self.assertEqual(expected, actual)

    def test_can_generate_multi_row_chart_from_pattern(self):
        pattern = Pattern([
            ExpandedRow(1, [
                Stitch("k"), Stitch("k"), Stitch("p"), Stitch("p"),
                Stitch("k"), Stitch("k"), Stitch("p"), Stitch("p"),
                Stitch("k"), Stitch("k")
            ]),
            ExpandedRow(2, [
                Stitch("k"),
                Stitch("k"), Stitch("k"), Stitch("p"), Stitch("p"),
                Stitch("k"), Stitch("k"), Stitch("p"), Stitch("p"),
                Stitch("k")
            ])
        ])
        chart = Chart(pattern)

        expected = (
            "---+---+---+---+---+---+---+---+---+---+---+---\n"
            " 2 | - | - | - |   |   | - | - |   |   | - |   \n"
            "---+---+---+---+---+---+---+---+---+---+---+---\n"
            "   |   |   | - | - |   |   | - | - |   |   | 1 \n"
            "---+---+---+---+---+---+---+---+---+---+---+---\n"
        )
        actual = chart.render_grid()

        self.assertEqual(expected, actual, f"expected was:\n{expected}\nactual was:\n{actual}")

    def test_can_pad_symmetrical_chart(self):
        # row 1: kfb, k2, kfb
        # row 2: p6
        # row 3: kfb, k4, kfb
        # row 4: p8
        pattern = Pattern([
            ExpandedRow(1, [
                Stitch("kfb"), Stitch("k"), Stitch("k"), Stitch("kfb")
            ]),
            ExpandedRow(2, [
                Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p")
            ]),
            ExpandedRow(3, [
                Stitch("kfb"), Stitch("k"), Stitch("k"), Stitch("k"), Stitch("k"), Stitch("kfb")
            ]),
            ExpandedRow(4, [
                Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p")
            ])
        ])
        chart = Chart(pattern)

        expected = (
            "---+---+---+---+---+---+---+---+---+---\n"
            " 4 |   |   |   |   |   |   |   |   |   \n"
            "---+---+---+---+---+---+---+---+---+---\n"
            "   | X | Y |   |   |   |   | Y | X | 3 \n"
            "---+---+---+---+---+---+---+---+---+---\n"
            " 2 | X |   |   |   |   |   |   | X |   \n"
            "---+---+---+---+---+---+---+---+---+---\n"
            "   | X | X | Y |   |   | Y | X | X | 1 \n"
            "---+---+---+---+---+---+---+---+---+---\n"
        )
        actual = chart.render_grid()

        self.assertEqual(expected, actual)

    # TODO: FIX CHART
    def test_can_pad_symmetrical_chart_2(self):
        self.maxDiff = None
        # row 1: ssk, k6, k2tog
        # row 2: p8
        # row 3: ssk, k4, k2tog
        # row 4: p6
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
            ])
        ])
        chart = Chart(pattern)
    
        expected = (
            "---+---+---+---+---+---+---+---+---+---\n"
            " 4 | X |   |   |   |   |   |   | X |   \n"
            "---+---+---+---+---+---+---+---+---+---\n"
            "   | X | / |   |   |   |   | \\ | X | 3 \n"
            "---+---+---+---+---+---+---+---+---+---\n"
            " 2 |   |   |   |   |   |   |   |   |   \n"
            "---+---+---+---+---+---+---+---+---+---\n"
            "   | / |   |   |   |   |   |   | \\ | 1 \n"
            "---+---+---+---+---+---+---+---+---+---\n"
        )
        actual = chart.render_grid()

        self.assertEqual(expected, actual, f"expected was:\n{expected}\nactual was:\n{actual}")

class TestKey(unittest.TestCase):
    def test_can_get_the_length_of_the_longest_column(self):
        ex_col_contents = ["Name", "Knit", "Purl"]
        junk_pattern = Pattern([ExpandedRow(1, [Stitch("k")])])
        chart = Chart(junk_pattern)

        expected = 6
        actual = chart._get_column_width(ex_col_contents)

        self.assertEqual(expected, actual)

    def test_can_pad_column_evenly(self):
        ex_col_contents = ["Name", "Knit", "Purl"]
        junk_pattern = Pattern([ExpandedRow(1, [Stitch("k")])])
        chart = Chart(junk_pattern)

        expected = [" Name ", " Knit ", " Purl "]
        actual = chart._pad_column(ex_col_contents)

        self.assertEqual(expected, actual)

    def test_can_generate_key_from_chart(self):
        pattern = Pattern([
            ExpandedRow(1, [Stitch("k"), Stitch("p"), Stitch("p"), Stitch("k")]),
            ExpandedRow(2, [Stitch("p"), Stitch("k"), Stitch("k"), Stitch("p")])
        ])
        chart = Chart(pattern)

        expected = (
            "+------+--------+-----------+-----------+\n"
            "| Name | Abbrev | RS Symbol | WS Symbol |\n"
            "+------+--------+-----------+-----------+\n"
            "| Knit |    k   |           |     -     |\n"
            "+------+--------+-----------+-----------+\n"
            "| Purl |    p   |     -     |           |\n"
            "+------+--------+-----------+-----------+\n"
        )
        actual = chart.render_key()

        self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()