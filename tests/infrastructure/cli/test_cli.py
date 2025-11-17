import subprocess
import unittest
from src.adapters.chart_adapter import ChartAdapter
from src.adapters.parser_adapter import ParserAdapter
from src.application.pattern_service import PatternService
from src.infrastructure.cli.cli_input_adapter import CLIAdapter

class TestCLI(unittest.TestCase):
    def test_can_generate_ascii_chart_from_adapter(self):
        parser_adapter = ParserAdapter()
        chart_adapter = ChartAdapter()
        service = PatternService(parser_adapter, chart_adapter)
        cli_adapter = CLIAdapter(pattern_service=service)

        actual = cli_adapter.run("k, p2, k")
        expected = (
            "Chart:\n"
            "---+---+---+---+---+---\n"
            "   |   | - | - |   | 1 \n"
            "---+---+---+---+---+---"
        )

        self.assertEqual(expected, actual)

    def test_can_generate_ascii_chart_from_cli(self):
        output = subprocess.run(
            ["python3", "-m", "src.infrastructure.cli.cli", "parse", "k, p, k"],
            capture_output=True,
            text=True
        )
        # print("STDOUT:", output.stdout)
        # print("STDERR:", output.stderr)
        # print("RETURN CODE:", output.returncode)
        
        self.assertEqual(0, output.returncode)
        expected_output = (
            "Chart:\n"
            "---+---+---+---+---\n"
            "   |   | - |   | 1 \n"
            "---+---+---+---+---"
        )
        actual_output = output.stdout.strip()
        self.assertEqual(expected_output, actual_output)

    def test_can_generate_ascii_chart_from_cli_package(self):
        output = subprocess.run(
            ["pattern_to_chart", "parse", "k, p, k"],
            capture_output=True,
            text=True
        )

        # print("STDOUT:", output.stdout)
        # print("STDERR:", output.stderr)
        # print("RETURN CODE:", output.returncode)

        self.assertEqual(0, output.returncode)
        expected_output = (
            "Chart:\n"
            "---+---+---+---+---\n"
            "   |   | - |   | 1 \n"
            "---+---+---+---+---"
        )
        actual_output = output.stdout.strip()
        self.assertEqual(expected_output, actual_output)

if __name__ == "__main__":
    unittest.main()