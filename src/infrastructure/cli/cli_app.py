import click
import textwrap
from src.adapters.chart_adapter import ChartAdapter
from src.adapters.parser_adapter import ParserAdapter
from src.application.pattern_service import PatternService
from src.infrastructure.cli.cli_input_adapter import CLIAdapter

def get_pattern():
    caston: int = 0
    rows: list[str] = []

    print("")
    print("*Note: Enter \"q\" to stop")
    print("")

    while True:
        raw_caston:str = click.prompt("Enter caston number")
        if raw_caston.isdigit():
            break
        if raw_caston == "q":
            return
        else:
            print("You didn't enter a number, please try again")
    
    caston = int(raw_caston)

    row_num = 1
    quitting = False
    while not quitting:
        row:str = click.prompt(f"Enter row {row_num}")
        if row.lower() == "q":
            break
        
        rows.append(row)
        row_num += 1
    
    full_pattern = f"Caston {caston} sts\n"
    for i, row in enumerate(rows):
        full_pattern += f"Row {i+1}: {row}\n"
    
    correct_prompt = "\nYou entered:\n" + full_pattern
    raw_correct:str = click.prompt(correct_prompt + textwrap.dedent(
        """
        Is this correct?
            (Y)es   [default]
            (N)o
        """
    ), default="y", show_default=False)
    is_correct = True

    if raw_correct not in ["", "y", "yes"]:
        is_correct = False

    if is_correct is False:
        get_pattern()

    parser_adapter = ParserAdapter()
    chart_adapter = ChartAdapter()
    service = PatternService(parser_adapter, chart_adapter)
    cli_adapter = CLIAdapter(pattern_service=service)
    print("\nGreat! Your pattern as a chart looks like: ")
    print(cli_adapter.run(full_pattern))

def main():
    raw_to_parse:str = click.prompt(textwrap.dedent(
        """
        Welcome!
        Do you want to parse a knitting pattern?
            (Y)es   [default]
            (N)o

        """
    ), default="y", show_default=False)
    to_parse:bool = True

    if raw_to_parse.lower() not in ["", "y", "yes"]:
        to_parse = False

    if to_parse is True:
        get_pattern()

if __name__ == "__main__":
    main()