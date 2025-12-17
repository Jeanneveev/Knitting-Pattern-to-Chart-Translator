import unittest
from src.domain.pattern.entities import Pattern, ExpandedRow, Stitch
from src.domain.chart.entities.chart import Chart, ChartRow, Cell, CellType, CellStitchType
from src.domain.renderer.ascii_renderer import ASCIIRender

SYMBOL = CellType.STITCH
EMPTY = CellType.EMPTY

R = CellStitchType.REGULAR
I = CellStitchType.INCREASE

class TestASCIIChart(unittest.TestCase):
    def test_can_pad_row_of_grid_1(self):
        self.maxDiff = None
        
        row_1 = ExpandedRow(1, [Stitch("k"), Stitch("kfb")])
        row_2 = ExpandedRow(2, [Stitch("p"), Stitch("p"), Stitch("p")])
        pattern = Pattern([row_1, row_2])
        chart = Chart(pattern)
        ascii_chart = ASCIIRender(chart)

        """ Chart should look like:
            "---+---+---+---+---\n"
            " 2 |   |   |   |   \n"
            "---+---+---+---+---\n"
            "   | X | Y |   | 1 \n"
            "---+---+---+---+---\n"
        """

        expected_row_1 = [Cell(EMPTY), Cell(SYMBOL, "Y", I), Cell(SYMBOL, " ", R)]
        expected_row_2 = [Cell(SYMBOL, " ", R), Cell(SYMBOL, " ", R), Cell(SYMBOL, " ", R)]
        actual = ascii_chart._pad_grid()
        actual_row_1 = actual[0].cells
        actual_row_2 = actual[1].cells

        self.assertEqual(expected_row_1, actual_row_1, f"\nexpected row 1 was:\n{expected_row_1}\nactual was:\n{actual_row_1}")
        self.assertEqual(expected_row_2, actual_row_2, f"\nexpected row 2 was:\n{expected_row_2}\nactual was:\n{actual_row_2}")

    # def test_can_pad_row_of_grid_2(self):
    #     self.maxDiff = None
        
    #     row_1 = ExpandedRow(1, [Stitch("k")])
    #     row_2 = ExpandedRow(2, [Stitch("yo"), Stitch("p")])
    #     pattern = Pattern([row_1, row_2])
    #     chart = Chart(pattern)
    #     ascii_chart = ASCIIRender(chart)

    #     """ Chart should look like:
    #         "---+---+---+---\n"
    #         " 2 | O |   |   \n"
    #         "---+---+---+---\n"
    #         "   | X |   | 1 \n"
    #         "---+---+---+---\n"
    #     """

    #     expected_row_1 = [Cell(EMPTY), Cell(SYMBOL, " ", REGULAR)]
    #     expected_row_2 = [Cell(SYMBOL, "O", INCREASE), Cell(SYMBOL, " ", REGULAR)]
    #     actual = ascii_chart._pad_grid()
    #     actual_row_1 = actual[0].cells
    #     actual_row_2 = actual[1].cells

    #     self.assertEqual(expected_row_1, actual_row_1, f"\nexpected row 1 was:\n{expected_row_1}\nactual was:\n{actual_row_1}")
    #     self.assertEqual(expected_row_2, actual_row_2, f"\nexpected row 2 was:\n{expected_row_2}\nactual was:\n{actual_row_2}")

    # def test_can_pad_row_of_grid_3(self):
    #     self.maxDiff = None
        
    #     row_1 = ExpandedRow(1, [Stitch("kfb")])
    #     row_2 = ExpandedRow(2, [Stitch("p"), Stitch("p")])
    #     pattern = Pattern([row_1, row_2])
    #     chart = Chart(pattern)
    #     ascii_chart = ASCIIRender(chart)

    #     """ Chart should look like:
    #         "---+---+---+---\n"
    #         " 2 |   | O |   \n"
    #         "---+---+---+---\n"
    #         "   |   | X | 1 \n"
    #         "---+---+---+---\n"
    #     """

    #     expected_row_1 = [Cell(SYMBOL, "Y", CellStitchType.INCREASE), Cell(EMPTY)]
    #     expected_row_2 = [Cell(SYMBOL, " ", CellStitchType.REGULAR), Cell(SYMBOL, " ", CellStitchType.REGULAR)]
    #     actual = ascii_chart._pad_grid()
    #     actual_row_1 = actual[0].cells
    #     actual_row_2 = actual[1].cells

    #     self.assertEqual(expected_row_1, actual_row_1, f"\nexpected row 1 was:\n{expected_row_1}\nactual was:\n{actual_row_1}")
    #     self.assertEqual(expected_row_2, actual_row_2, f"\nexpected row 2 was:\n{expected_row_2}\nactual was:\n{actual_row_2}")


    # def test_can_pad_symmetrical_chart_increasing(self):
    #     # row 1: kfb, k2, kfb
    #     # row 2: p6
    #     # row 3: kfb, k4, kfb
    #     # row 4: p8

    #     self.maxDiff = None

    #     row_1 = ExpandedRow(5, [
    #         Stitch("kfb"), Stitch("k"), Stitch("k"), Stitch("kfb")
    #     ])
    #     row_2 = ExpandedRow(6, [
    #         Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p")
    #     ])
    #     row_3 = ExpandedRow(7, [
    #         Stitch("kfb"), Stitch("k"), Stitch("k"), Stitch("k"), Stitch("k"), Stitch("kfb")
    #     ])
    #     row_4 = ExpandedRow(8, [
    #         Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p")
    #     ])
    #     pattern = Pattern([row_1, row_2, row_3, row_4])
    #     chart = Chart(pattern)
    #     ascii_chart = ASCIIRender(chart)

    #     """ Chart should look like:
    #         "---+---+---+---+---+---+---+---+---+---\n"
    #         " 8 |   |   |   |   |   |   |   |   |   \n"
    #         "---+---+---+---+---+---+---+---+---+---\n"
    #         "   | X | Y |   |   |   |   | Y | X | 7 \n"
    #         "---+---+---+---+---+---+---+---+---+---\n"
    #         " 6 | X |   |   |   |   |   |   | X |   \n"
    #         "---+---+---+---+---+---+---+---+---+---\n"
    #         "   | X | X | Y |   |   | Y | X | X | 5 \n"
    #         "---+---+---+---+---+---+---+---+---+---\n"
    #     """
    #     expected_row_1 = [
    #         Cell(EMPTY), Cell(EMPTY),
    #         Cell(SYMBOL, "Y", CellStitchType.INCREASE),
    #         Cell(SYMBOL, " ", CellStitchType.REGULAR), Cell(SYMBOL, " ", CellStitchType.REGULAR),
    #         Cell(SYMBOL, "Y", CellStitchType.INCREASE),
    #         Cell(EMPTY), Cell(EMPTY)
    #     ]
    #     expected_row_2 = [
    #         Cell(EMPTY),
    #         Cell(SYMBOL, " ", CellStitchType.REGULAR), Cell(SYMBOL, " ", CellStitchType.REGULAR),
    #         Cell(SYMBOL, " ", CellStitchType.REGULAR), Cell(SYMBOL, " ", CellStitchType.REGULAR),
    #         Cell(SYMBOL, " ", CellStitchType.REGULAR), Cell(SYMBOL, " ", CellStitchType.REGULAR),
    #         Cell(EMPTY)
    #     ]
    #     expected_row_3 = [
    #         Cell(EMPTY),
    #         Cell(SYMBOL, "Y", CellStitchType.INCREASE),
    #         Cell(SYMBOL, " ", CellStitchType.REGULAR), Cell(SYMBOL, " ", CellStitchType.REGULAR),
    #         Cell(SYMBOL, " ", CellStitchType.REGULAR), Cell(SYMBOL, " ", CellStitchType.REGULAR),
    #         Cell(SYMBOL, "Y", CellStitchType.INCREASE),
    #         Cell(EMPTY)
    #     ]
    #     expected_row_4 = [
    #         Cell(SYMBOL, " ", CellStitchType.REGULAR), Cell(SYMBOL, " ", CellStitchType.REGULAR),
    #         Cell(SYMBOL, " ", CellStitchType.REGULAR), Cell(SYMBOL, " ", CellStitchType.REGULAR),
    #         Cell(SYMBOL, " ", CellStitchType.REGULAR), Cell(SYMBOL, " ", CellStitchType.REGULAR),
    #         Cell(SYMBOL, " ", CellStitchType.REGULAR), Cell(SYMBOL, " ", CellStitchType.REGULAR),
    #     ]

    #     actual = ascii_chart._pad_grid()
    #     actual_row_1 = actual[0].cells
    #     actual_row_2 = actual[1].cells
    #     actual_row_3 = actual[2].cells
    #     actual_row_4 = actual[3].cells

    #     self.assertEqual(expected_row_1, actual_row_1, f"\nexpected row 1 was:\n{expected_row_1}\nactual was:\n{actual_row_1}")
    #     self.assertEqual(expected_row_2, actual_row_2, f"\nexpected row 2 was:\n{expected_row_2}\nactual was:\n{actual_row_2}")
    #     self.assertEqual(expected_row_3, actual_row_3, f"\nexpected row 3 was:\n{expected_row_3}\nactual was:\n{actual_row_3}")
    #     self.assertEqual(expected_row_4, actual_row_4, f"\nexpected row 4 was:\n{expected_row_4}\nactual was:\n{actual_row_4}")

    # def test_can_pad_symmetrical_chart_increasing_2(self):
    #     # row 1: k
    #     # row 2: yo, k, yo
    #     # row 3: k3
    #     # row 4: yo, k3, yo
    #     # row 5: k5



    # def test_can_pad_symmetrical_chart_decreasing(self):
    #     self.maxDiff = None
    #     # row 1: ssk, k6, k2tog
    #     # row 2: p8
    #     # row 3: ssk, k4, k2tog
    #     # row 4: p6
    #     # row 5: ssk, k2, k2tog
    #     pattern = Pattern([
    #         ExpandedRow(1, [
    #             Stitch("ssk"),
    #             Stitch("k"), Stitch("k"), Stitch("k"), Stitch("k"), Stitch("k"), Stitch("k"),
    #             Stitch("k2tog")
    #         ]),
    #         ExpandedRow(2, [
    #             Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p")
    #         ]),
    #         ExpandedRow(3, [
    #             Stitch("ssk"),
    #             Stitch("k"), Stitch("k"), Stitch("k"), Stitch("k"),
    #             Stitch("k2tog")
    #         ]),
    #         ExpandedRow(4, [
    #             Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p")
    #         ]),
    #         ExpandedRow(5, [
    #             Stitch("ssk"),
    #             Stitch("k"), Stitch("k"),
    #             Stitch("k2tog")
    #         ])
    #     ])
    #     chart = Chart(pattern)
    #     ascii_chart = ASCIIRender(chart)
    
    #     """ Chart should look like:
    #         "---+---+---+---+---+---+---+---+---+---\n"
    #         "   | X | X | / |   |   | \\ | X | X | 5 \n"
    #         "---+---+---+---+---+---+---+---+---+---\n"
    #         " 4 | X |   |   |   |   |   |   | X |   \n"
    #         "---+---+---+---+---+---+---+---+---+---\n"
    #         "   | X | / |   |   |   |   | \\ | X | 3 \n"
    #         "---+---+---+---+---+---+---+---+---+---\n"
    #         " 2 |   |   |   |   |   |   |   |   |   \n"
    #         "---+---+---+---+---+---+---+---+---+---\n"
    #         "   | / |   |   |   |   |   |   | \\ | 1 \n"
    #         "---+---+---+---+---+---+---+---+---+---\n"
    #     """
    #     expected_row_1 = [
    #         Cell(CellType.STITCH, "/", CellStitchType.DECREASE),
    #         Cell(CellType.STITCH, " ", CellStitchType.REGULAR), Cell(CellType.STITCH, " ", CellStitchType.REGULAR),
    #         Cell(CellType.STITCH, " ", CellStitchType.REGULAR), Cell(CellType.STITCH, " ", CellStitchType.REGULAR),
    #         Cell(CellType.STITCH, " ", CellStitchType.REGULAR), Cell(CellType.STITCH, " ", CellStitchType.REGULAR),
    #         Cell(CellType.STITCH, "\\", CellStitchType.DECREASE)
    #     ]
    #     expected_row_2 = [
    #         Cell(CellType.STITCH, " ", CellStitchType.REGULAR), Cell(CellType.STITCH, " ", CellStitchType.REGULAR),
    #         Cell(CellType.STITCH, " ", CellStitchType.REGULAR), Cell(CellType.STITCH, " ", CellStitchType.REGULAR),
    #         Cell(CellType.STITCH, " ", CellStitchType.REGULAR), Cell(CellType.STITCH, " ", CellStitchType.REGULAR),
    #         Cell(CellType.STITCH, " ", CellStitchType.REGULAR), Cell(CellType.STITCH, " ", CellStitchType.REGULAR)
    #     ]
    #     expected_row_3 = [
    #         Cell(EMPTY),
    #         Cell(CellType.STITCH, "/", CellStitchType.DECREASE),
    #         Cell(CellType.STITCH, " ", CellStitchType.REGULAR), Cell(CellType.STITCH, " ", CellStitchType.REGULAR),
    #         Cell(CellType.STITCH, " ", CellStitchType.REGULAR), Cell(CellType.STITCH, " ", CellStitchType.REGULAR),
    #         Cell(CellType.STITCH, "\\", CellStitchType.DECREASE),
    #         Cell(EMPTY)
    #     ]
    #     expected_row_4 = [
    #         Cell(EMPTY),
    #         Cell(CellType.STITCH, " ", CellStitchType.REGULAR), Cell(CellType.STITCH, " ", CellStitchType.REGULAR),
    #         Cell(CellType.STITCH, " ", CellStitchType.REGULAR), Cell(CellType.STITCH, " ", CellStitchType.REGULAR),
    #         Cell(CellType.STITCH, " ", CellStitchType.REGULAR), Cell(CellType.STITCH, " ", CellStitchType.REGULAR),
    #         Cell(EMPTY)
    #     ]
    #     expected_row_5 = [
    #         Cell(EMPTY), Cell(EMPTY),
    #         Cell(CellType.STITCH, "/", CellStitchType.DECREASE),
    #         Cell(CellType.STITCH, " ", CellStitchType.REGULAR), Cell(CellType.STITCH, " ", CellStitchType.REGULAR),
    #         Cell(CellType.STITCH, "\\", CellStitchType.DECREASE),
    #         Cell(EMPTY), Cell(EMPTY)
    #     ]

    #     actual = ascii_chart._pad_grid()
    #     actual_row_1 = actual[0].cells
    #     actual_row_2 = actual[1].cells
    #     actual_row_3 = actual[2].cells
    #     actual_row_4 = actual[3].cells
    #     actual_row_5 = actual[4].cells

    #     self.assertEqual(expected_row_1, actual_row_1, f"\nexpected row 1 was:\n{expected_row_1}\nactual was:\n{actual_row_1}")
    #     self.assertEqual(expected_row_2, actual_row_2, f"\nexpected row 2 was:\n{expected_row_2}\nactual was:\n{actual_row_2}")
    #     self.assertEqual(expected_row_3, actual_row_3, f"\nexpected row 3 was:\n{expected_row_3}\nactual was:\n{actual_row_3}")
    #     self.assertEqual(expected_row_4, actual_row_4, f"\nexpected row 4 was:\n{expected_row_4}\nactual was:\n{actual_row_4}")
    #     self.assertEqual(expected_row_5, actual_row_5, f"\nexpected row 5 was:\n{expected_row_5}\nactual was:\n{actual_row_5}")

if __name__ == "__main__":
    unittest.main()