import subprocess
import unittest
from src.adapters.chart_adapter import ChartAdapter
from src.adapters.parser_adapter import ParserAdapter
from src.application.pattern_service import PatternService
from src.infrastructure.cli.cli_input_adapter import CLIAdapter

class TestCLIAdapter(unittest.TestCase):
    def test_can_generate_ascii_chart_from_adapter(self):
        parser_adapter = ParserAdapter()
        chart_adapter = ChartAdapter()
        service = PatternService(parser_adapter, chart_adapter)
        cli_adapter = CLIAdapter(pattern_service=service)

        actual = cli_adapter.chart_only("k, p2, k")
        expected = (
            "Chart:\n"
            "---+---+---+---+---+---\n"
            "   |   | - | - |   | 1 \n"
            "---+---+---+---+---+---"
        )

        self.assertEqual(expected, actual)

    def test_can_generate_ascii_chart_and_key_from_adapter(self):
        self.maxDiff = None

        parser_adapter = ParserAdapter()
        chart_adapter = ChartAdapter()
        service = PatternService(parser_adapter, chart_adapter)
        cli_adapter = CLIAdapter(pattern_service=service)
        pattern = "p, yo, k2tog, yo, k2tog, yo, p"

        actual = cli_adapter.run(pattern)
        expected = (
            "Chart:\n"
            "---+---+---+---+---+---+---+---+---\n"
            "   | - | O | / | O | / | O | - | 1 \n"
            "---+---+---+---+---+---+---+---+---\n"
            "\n"
            "Key:\n"
            "+-----------------+--------+-----------+-----------+\n"
            "|       Name      | Abbrev | RS Symbol | WS Symbol |\n"
            "+-----------------+--------+-----------+-----------+\n"
            "|       Purl      |    p   |     -     |           |\n"
            "+-----------------+--------+-----------+-----------+\n"
            "|    Yarn Over    |   yo   |     O     |     O     |\n"
            "+-----------------+--------+-----------+-----------+\n"
            "| Knit 2 Together |  k2tog |     /     |     /     |\n"
            "+-----------------+--------+-----------+-----------+\n"
        )
        
        self.assertEqual(expected, actual)

class TestCLI(unittest.TestCase):
    def test_can_generate_ascii_chart_from_cli(self):
        output = subprocess.run(
            ["python3", "-m", "src.infrastructure.cli.cli", "parse", "--chart_only", "k, p, k"],
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

    def test_can_generate_ascii_chart_and_key_from_cli(self):
        self.maxDiff = None

        output = subprocess.run(
            ["python3", "-m", "src.infrastructure.cli.cli", "parse", "k, p, k"],
            capture_output=True,
            text=True
        )

        self.assertEqual(0, output.returncode)
        expected_output = (
            "Chart:\n"
            "---+---+---+---+---\n"
            "   |   | - |   | 1 \n"
            "---+---+---+---+---\n"
            "\n"
            "Key:\n"
            "+------+--------+-----------+-----------+\n"
            "| Name | Abbrev | RS Symbol | WS Symbol |\n"
            "+------+--------+-----------+-----------+\n"
            "| Knit |    k   |           |     -     |\n"
            "+------+--------+-----------+-----------+\n"
            "| Purl |    p   |     -     |           |\n"
            "+------+--------+-----------+-----------+\n"
        )
        actual_output = output.stdout.strip()+"\n"  # NOTE: .strip() strips trailing newline
        self.assertEqual(expected_output, actual_output)

class TestCLIPackage(unittest.TestCase):
    def test_can_generate_ascii_chart_from_cli_package(self):
        output = subprocess.run(
            ["pattern_to_chart", "parse", "--chart_only", "k2, p, k"],
            capture_output=True,
            text=True
        )

        # print("STDOUT:", output.stdout)
        # print("STDERR:", output.stderr)
        # print("RETURN CODE:", output.returncode)

        self.assertEqual(0, output.returncode)
        expected_output = (
            "Chart:\n"
            "---+---+---+---+---+---\n"
            "   |   | - |   |   | 1 \n"
            "---+---+---+---+---+---"
        )
        actual_output = output.stdout.strip()
        self.assertEqual(expected_output, actual_output)

    def test_can_generate_ascii_chart_and_key_from_cli_package(self):
        self.maxDiff = None

        output = subprocess.run(
            ["pattern_to_chart", "parse", "p, k2, p2, k"],
            capture_output=True,
            text=True
        )

        self.assertEqual(0, output.returncode)
        expected_output = (
            "Chart:\n"
            "---+---+---+---+---+---+---+---\n"
            "   |   | - | - |   |   | - | 1 \n"
            "---+---+---+---+---+---+---+---\n"
            "\n"
            "Key:\n"
            "+------+--------+-----------+-----------+\n"
            "| Name | Abbrev | RS Symbol | WS Symbol |\n"
            "+------+--------+-----------+-----------+\n"
            "| Purl |    p   |     -     |           |\n"
            "+------+--------+-----------+-----------+\n"
            "| Knit |    k   |           |     -     |\n"
            "+------+--------+-----------+-----------+\n"
        )
        actual_output = output.stdout.strip()+"\n"
        self.assertEqual(expected_output, actual_output)

if __name__ == "__main__":
    unittest.main()