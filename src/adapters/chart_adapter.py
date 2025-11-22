from src.domain import Part, Pattern, PatternBuilder, Chart
from src.ports.chart_port import ChartPort

class ChartAdapter(ChartPort):
    def __init__(self):
        self.latest_chart = None

    def render_chart(self, model:Part) -> str:
        pattern = PatternBuilder(model).build_pattern()
        chart = Chart(pattern)
        return chart.render_grid()
    
    def render_key(self, model:Part) -> str:
        pattern = PatternBuilder(model).build_pattern()
        chart = Chart(pattern)
        return chart.render_key()