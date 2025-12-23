from abc import ABC, abstractmethod
from src.domain import Pattern

class ChartPort(ABC):
    def __init__(self):
        self.latest_chart = None

    @abstractmethod
    def render_chart(self, pattern:Pattern) -> str:
        pass

    @abstractmethod
    def render_key(self, pattern:Pattern) -> str:
        pass