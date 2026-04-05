class DebugTrace:

    def __init__(self):
        self.steps = []

    def add(self, step, data):
        self.steps.append({
            "step": step,
            "data": data
        })

    def get(self):
        return self.steps