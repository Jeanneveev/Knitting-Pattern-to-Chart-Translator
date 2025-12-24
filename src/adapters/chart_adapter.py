from src.domain import ASCIIRender, Chart, Pattern
from src.ports.chart_port import ChartPort

class ChartingError(Exception): 
    """Exception raised for errors during the charting process"""
    def __init__(self, message): 
        super().__init__(message)

class ChartAdapter(ChartPort):
    def __init__(self):
        self.latest_chart = None

    def render_chart(self, pattern:Pattern) -> str:
        try:
            chart = Chart(pattern)
        except Exception as e:
            raise ChartingError(f"Error occured when building chart: {repr(e)}") from e
        
        renderer = ASCIIRender(chart)
        return renderer.render_chart()
    
    def render_key(self, pattern:Pattern) -> str:
        try:
            chart = Chart(pattern)
        except Exception as e:
            raise ChartingError(f"Error occured when building chart: {repr(e)}") from e
        
        try:
            renderer = ASCIIRender(chart)
        except Exception as e:
            raise ChartingError(f"Error occured when rendering ASCII chart: {repr(e)}") from e
        return renderer.render_key()
        
