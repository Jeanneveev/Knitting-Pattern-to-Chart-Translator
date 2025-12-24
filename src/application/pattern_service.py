from src.adapters.chart_adapter import ChartAdapter
from src.adapters.parser_adapter import ParserAdapter
from src.adapters.logging.logger_adapter import get_logger
logger = get_logger("pattern_service")

class PatternService():
    """Use case: Given a knitting pattern, can produce a corresponding ASCII knitting chart"""
    def __init__(self, parser_adapter:ParserAdapter, chart_adapter:ChartAdapter):
        self.parser_adapter = parser_adapter
        self.chart_adapter = chart_adapter
    
    def generate_chart(self, input:str) -> str:
        logger.info("Parsing input")
        try:
            model = self.parser_adapter.parse(input)
        except Exception as e:
            logger.error(e)
            raise(e)
        
        logger.info("Creating chart")
        chart:str = self.chart_adapter.render_chart(model)

        self.chart_adapter.latest_chart = chart
        return chart
    
    def generate_key(self, input:str) -> str:
        logger.info("Generate key called")
        model = self.parser_adapter.parse(input)
        key:str = self.chart_adapter.render_key(model)

        return key