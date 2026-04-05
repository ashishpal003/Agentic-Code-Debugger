class ConfidenceScorer:

    def score(self, initial_error, final_result, iterations):
        score = 0.0

        # code runs successfully
        if final_result.get("success"):
            score += 0.5

        # Error resolved
        if initial_error and not final_result.get("stderr"):
            score += 0.3
        
        # Fewer iterations = better
        if iterations == 1:
            score += 0.2
        elif iterations <= 3:
            score += 0.1
        
        return round(score, 2)