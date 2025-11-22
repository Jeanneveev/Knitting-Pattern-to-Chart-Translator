from src.application.pattern_service import PatternService

class CLIAdapter():
    def __init__(self, pattern_service:PatternService):
        self.pattern_service = pattern_service

    def run(self, pattern:str):
        chart = f"Chart:\n{self.pattern_service.generate_chart(pattern)}"
        key = f"Key:\n{self.pattern_service.generate_key(pattern)}"
        return chart+"\n"+key
    
    def chart_only(self, pattern:str):
        return f"Chart:\n{self.pattern_service.generate_chart(pattern)}"
    
    def key_only(self, pattern:str):
        return f"Key:\n{self.pattern_service.generate_key(pattern)}"