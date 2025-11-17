import unittest
from src.application.pattern_service import PatternService
from src.adapters.parser_adapter import ParserAdapter
from src.adapters.chart_adapter import ChartAdapter

class TestPatternService(unittest.TestCase):
    def test_can_parse_and_generate_chart(self):
        parser_adapter = ParserAdapter()
        chart_adapter = ChartAdapter()
        pattern_service = PatternService(parser_adapter, chart_adapter)
        pattern = "k2, p2"

        expected = (
            "---+---+---+---+---+---\n"
            "   | - | - |   |   | 1 \n"
            "---+---+---+---+---+---"
        )
        actual = pattern_service.generate_chart(input=pattern)

        self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()