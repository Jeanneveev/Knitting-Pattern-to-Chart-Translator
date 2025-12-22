from abc import ABC, abstractmethod
from src.domain import Pattern

class ParserPort(ABC):
    @abstractmethod
    def parse(self, pattern:str) -> Pattern:
        """Parse a string pattern into a Pattern"""
        pass
