from src.domain.model.model import Part, Chart
from src.ports.chart_port import ChartPort

class ChartAdapter(ChartPort):
    def __init__(self):
        self.latest_chart = None

    def render_chart(self, model:Part) -> str:
        chart = Chart(model)
        return chart.render_grid()
    
    def render_key(self, model:Part) -> str:
        chart = Chart(model)
        return chart.render_key()