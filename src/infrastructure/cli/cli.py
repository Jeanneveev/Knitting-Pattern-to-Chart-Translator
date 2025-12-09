import click
from src.infrastructure.cli.cli_input_adapter import CLIAdapter
from src.adapters.chart_adapter import ChartAdapter
from src.adapters.parser_adapter import ParserAdapter
from src.application.pattern_service import PatternService
from src.infrastructure.cli.cli_app import main

@click.group()
def cli():
    """Command line tool for translating knitting patterns to ASCII charts"""
    pass

@click.command(name="parse")
@click.option("--chart_only", is_flag=True, help="Display only the knitting chart")
@click.option("--key_only", is_flag=True, help="Display only the knitting chart key")
@click.argument("pattern", type=str)
def parse(chart_only, key_only, pattern:str):
    """Parse pattern text"""
    parser_adapter = ParserAdapter()
    chart_adapter = ChartAdapter()
    service = PatternService(parser_adapter, chart_adapter)
    cli_adapter = CLIAdapter(pattern_service=service)

    if chart_only:
        output = cli_adapter.chart_only(pattern)
    elif key_only:
        output = cli_adapter.key_only(pattern)
    else:
        output = cli_adapter.run(pattern)

    click.echo(output)

@click.command(name="start")
def start():
    main()

cli.add_command(parse)
cli.add_command(start)

if __name__ == "__main__":
    cli()