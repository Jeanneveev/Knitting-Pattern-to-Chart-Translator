from src.domain import ASCIIRender, Chart, Pattern
from src.ports.chart_port import ChartPort

class ChartAdapter(ChartPort):
    def __init__(self):
        self.latest_chart = None

    def render_chart(self, pattern:Pattern) -> str:
        try:
            chart = Chart(pattern)
        except Exception as err:
            raise AttributeError(f"Error occured when building chart:\n{repr(err)}") from err
        
        renderer = ASCIIRender(chart)
        return renderer.render_chart()
    
    def render_key(self, pattern:Pattern) -> str:
        try:
            chart = Chart(pattern)
        except Exception as err:
            raise AttributeError(f"Error occured when building chart:\n{repr(err)}") from err
        
