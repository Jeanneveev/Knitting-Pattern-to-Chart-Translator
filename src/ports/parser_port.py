from abc import ABC, abstractmethod
from src.domain.model.model import Chart

class ParserPort(ABC):
    @abstractmethod
    def parse(self, pattern:str) -> Chart:
        pass
