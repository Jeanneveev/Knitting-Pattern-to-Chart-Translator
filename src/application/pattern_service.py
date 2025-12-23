from src.ports.chart_port import ChartPort
from src.ports.parser_port import ParserPort
from src.adapters.logging.logger_adapter import get_logger
logger = get_logger("pattern_service")

class PatternService():
    """Use case: Given a knitting pattern, can produce a corresponding ASCII knitting chart"""
    def __init__(self, parser_port:ParserPort, chart_port:ChartPort):
        self.parser_port = parser_port
        self.chart_port = chart_port
    
    def generate_chart(self, input:str) -> str:
        logger.info("Generate chart called")
        model = self.parser_port.parse(input)
        chart:str = self.chart_port.render_chart(model)

        self.chart_port.latest_chart = chart
        return chart
    
    def generate_key(self, input:str) -> str:
        logger.info("Generate key called")
        model = self.parser_port.parse(input)
        key:str = self.chart_port.render_key(model)

        return key