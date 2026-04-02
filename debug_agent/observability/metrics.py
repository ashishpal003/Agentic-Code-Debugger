class Metrics:
    def __init__(self):
        self.data = {
            "iterations": 0,
            "errors": [],
            "success": False
        }

    def record_iteration(self):
        self.data["iterations"] += 1

    def record_errors(self, error):
        self.data["errors"].append(error)
    
    def mark_success(self):
        self.data["success"] = True

    def get_metrics(self):
        return self.data
