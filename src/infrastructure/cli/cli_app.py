import click
import textwrap
from src.adapters.chart_adapter import ChartAdapter
from src.adapters.parser_adapter import ParserAdapter
from src.application.pattern_service import PatternService
from src.infrastructure.cli.cli_input_adapter import CLIAdapter

# NOTE: Because the caston number is the only real thing I can validate at this level, these functions aren't necessary
# But they work
def validate_input(prompt:str, message:str, validator):
    is_valid = False
    while True:
        value = click.prompt(prompt)
        is_valid = validator(value)
        if is_valid:
            break
        else:
            print(message)
    return value

def is_integer(string:str):
    return string.isdigit()

def get_pattern():
    caston: int = 0
    rows: list[str] = []

    print("")
    print("*Note: Enter \"q\" to stop")
    print("")

    caston = int(validate_input(
        "Enter caston number: ",
        "You didn't enter a number, please try again",
        is_integer
    ))
    
    row_num = 1
    quitting = False
    while not quitting:
        row:str = click.prompt(f"Enter row {row_num}: ")
        if row.lower() == "q":
            break
        
        rows.append(row)
        row_num += 1
    
    full_pattern = f"Caston {caston} sts\n"
    for i, row in enumerate(rows):
        full_pattern += f"Row {i+1}: {row}\n"
    
    raw_correct:str = click.prompt(textwrap.dedent(
        f"""
        You entered:
        {full_pattern}

        Is this correct?
            (Y)es   [default]
            (N)o
        """
    ))
    is_correct = True

    if raw_correct not in ["", "y", "yes"]:
        is_correct = False

    if is_correct is False:
        get_pattern()

    parser_adapter = ParserAdapter()
    chart_adapter = ChartAdapter()
    service = PatternService(parser_adapter, chart_adapter)
    cli_adapter = CLIAdapter(pattern_service=service)
    print("Great! Your pattern as a chart looks like: ")
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