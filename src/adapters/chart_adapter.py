from src.domain.model.model import Part, Chart
from src.ports.chart_port import ChartPort

class ChartAdapter(ChartPort):
    def render_chart(self, model:Part) -> str:
        chart = Chart(model)
        return chart.render_grid()