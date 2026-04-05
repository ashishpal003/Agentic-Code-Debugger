class ErrorClassifier:
    """
    Classifies Python errors into categories for agent decision making.
    """

    def classify(self, error: str):

        if "SyntaxError" in error:
            return "syntax_error"

        if "ModuleNotFoundError" in error:
            return "missing_dependency"
        
        if "ImportError" in error:
            return "missing_dependency"
        
        return "unknown"