class ErrorClassifier:

    def classify(self, error: str):

        if "ModuleNotFoundError" in error:
            return "missing_dependency"
        
        if "ImportError" in error:
            return "missing_dependency"
        
        if "SyntaxError" in error:
            return "syntax_error"
        
        return "unknown"