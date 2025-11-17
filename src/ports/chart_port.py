from abc import ABC, abstractmethod
from src.domain.model.model import Part

class ChartPort(ABC):
    def __init__(self):
        self.latest_chart = None

    @abstractmethod
    def render_chart(self, model:Part) -> str:
        pass