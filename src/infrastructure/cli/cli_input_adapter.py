from src.application.pattern_service import PatternService

class CLIAdapter():
    def __init__(self, pattern_service:PatternService):
        self.pattern_service = pattern_service

    def run(self, pattern:str):
        return f"Chart:\n{self.pattern_service.generate_chart(pattern)}"