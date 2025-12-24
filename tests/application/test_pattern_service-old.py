import unittest
from unittest.mock import Mock
from src.application.pattern_service import PatternService
from src.ports.chart_port import ChartPort
from src.ports.parser_port import ParserPort

class TestIntegrationPatternService(unittest.TestCase):
    def test_generate_chart_calls_correct_ports(self):
        mock_parser_port = Mock(spec=ParserPort)
        mock_parser_port.parse.return_value = "[model here]"

        mock_chart_port = Mock(spec=ChartPort)
        mock_chart_port.render_chart.return_value = "[chart here]"

        service = PatternService(parser_adapter=mock_parser_port, chart_adapter=mock_chart_port)

        pattern = "k2, p2"
        chart = service.generate_chart(pattern)

        mock_parser_port.parse.assert_called_once_with("k2, p2")
        mock_chart_port.render_chart.assert_called_once_with("[model here]")

class TestUnitPatternService(unittest.TestCase):
    def test_pattern_service_must_be_initialized_parser_and_chart_port_instances(self):
        try:
            mock_parser_port = Mock(spec=ParserPort)
            mock_chart_port = Mock(spec=ChartPort)
            service = PatternService(parser_adapter=mock_parser_port, chart_adapter=mock_chart_port)
        except Exception:
            self.fail("PatternService instance failed to be created")

        with self.assertRaises(TypeError) as err:
            bad_service = PatternService()
        self.assertEqual("PatternService.__init__() missing 2 required positional arguments: 'parser_port' and 'chart_port'", str(err.exception))

    def test_generate_chart_calls_parser_port(self):
        mock_parser_port = Mock(spec=ParserPort)
        mock_chart_port = Mock(spec=ChartPort)

        mock_parser_port.parse.return_value = "[model here]"

        service = PatternService(parser_adapter=mock_parser_port, chart_adapter=mock_chart_port)
        service.generate_chart("k2, p2")

        mock_parser_port.parse.assert_called_once_with("k2, p2")

    def test_generate_chart_calls_chart_port(self):
        ...    

    def test_generate_chart_saves_chart_to_chart_port(self):
        mock_parser_port = Mock(spec=ParserPort)
        mock_parser_port.parse.return_value = "[model here]"
        mock_chart_port = Mock(spec=ChartPort)
        mock_chart_port.render_chart.return_value = "[chart here]"
        service = PatternService(parser_adapter=mock_parser_port, chart_adapter=mock_chart_port)

        pattern = "k, p, k"
        chart = service.generate_chart(pattern)

        expected = chart
        actual = mock_chart_port.latest_chart

        self.assertEqual(expected, actual)
        

    # def test_can_parse_and_generate_chart(self):
    #     pattern_service = PatternService()
    #     pattern = "k2, p2"

    #     expected = (
    #         "---+---+---+---+---+---\n"
    #         "   | - | - |   |   | 1 \n"
    #         "---+---+---+---+---+---"
    #     )
    #     actual = pattern_service.generate_chart(input=pattern)

    #     self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()