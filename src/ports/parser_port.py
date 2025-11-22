from abc import ABC, abstractmethod
from src.domain import Part

class ParserPort(ABC):
    @abstractmethod
    def parse(self, pattern:str) -> Part:
        """Parse a string pattern into a Part"""
        pass
