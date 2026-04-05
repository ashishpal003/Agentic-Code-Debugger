class ConfidenceScorer:
    """
    Computes confidence score for debugging result.
    """

    def score(self, initial_error: str, final_result: dict, iterations: int) -> float:
        score = 0.0

        # Successful execution
        if final_result.get("success"):
            score += 0.5

        # Error resolved
        if initial_error and not final_result.get("stderr"):
            score += 0.3
        
        # Efficiency bonus
        if iterations == 1:
            score += 0.2
        elif iterations <= 3:
            score += 0.1
        
        return round(score, 2)